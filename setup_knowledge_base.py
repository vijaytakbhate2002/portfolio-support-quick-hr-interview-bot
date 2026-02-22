from rag_assisted_bot.rag_assisted_chatbot import build_vectordb, github_scrapper
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Configuration
USERNAME = 'vijaytakbhate2002'
GITHUB_DATA_DIR = './github_data'
README_FILES_DIR = os.path.join(GITHUB_DATA_DIR, 'readme_files')
METADATA_FILE = os.path.join(GITHUB_DATA_DIR, 'metadata.json')
METADATA_FILE_UPDATED = os.path.join(GITHUB_DATA_DIR, 'metadata_updated.json')
VECTORDB_PATH = "./vector_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "my_embeddings"


def replace_none_with_string(data):
    """
    Recursively replaces all None values with the string "NONE".
    Works for dicts, lists, tuples, and nested structures.
    """
    if isinstance(data, dict):
        return {
            key: replace_none_with_string(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [replace_none_with_string(item) for item in data]
    elif isinstance(data, tuple):
        return tuple(replace_none_with_string(item) for item in data)
    elif data is None:
        return "NONE"
    else:
        return data
    

def setup():
    print("Starting GitHub Scraping...")
    # Ensure directories exist
    os.makedirs(README_FILES_DIR, exist_ok=True)
    
    # Initialize and run scraper
    scrapper = github_scrapper.GithubScrapper(
        username=USERNAME, 
        save_folder=README_FILES_DIR, 
        metadata_save_folder=METADATA_FILE
    )
    scrapper.scrap()
    print("Scraping completed.")

    print("Building Vector Database...")
    # Initialize and run vector DB builder
    builder = build_vectordb.BuildVectorDB(
        directory_path=README_FILES_DIR,
        vectordb_path=VECTORDB_PATH,
        embedding_model_name=EMBEDDING_MODEL,
        collection_name=COLLECTION_NAME,
        metadatas_path=METADATA_FILE_UPDATED,
        chunk_size=300,
        chunk_overlap=50
    )
    chunks, document_names = builder.split_documents(
        documents=builder.load_documents()
    )

    # print("document_names: ", document_names)

    # let's update the sequence of metadata.json to match it with the document sequence
    pdf_names = [USERNAME + "/" + doc.split("\\")[-1].replace(".pdf", "") for doc in document_names]
    with open(METADATA_FILE, 'r') as f:
        metadata = json.load(f)
        metadata = metadata.get("github", [])

    # Reorder metadata to match the order of PDFs
    reordered_metadata = []
    for pdf_name in pdf_names:
        found_match = False
        for data in metadata:
            if pdf_name.strip().lower() == data['full_name'].strip().lower():
                data = replace_none_with_string(data)
                reordered_metadata.append(data)
                found_match = True
        if not found_match:
            raise ValueError(f"No matching metadata found for PDF: {pdf_name}")

    # Write reordered metadata back to file
    with open(METADATA_FILE_UPDATED, 'w') as f:
        json.dump({"github": reordered_metadata}, f, indent=2)

    builder.build(chunks, metadatas=reordered_metadata)
    print("Vector Database built successfully.")

if __name__ == "__main__":
    setup()
