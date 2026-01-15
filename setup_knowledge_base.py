from rag_assisted_bot.rag_assisted_chatbot import build_vectordb, github_scrapper
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration
USERNAME = 'vijaytakbhate2002'
GITHUB_DATA_DIR = './github_data'
README_FILES_DIR = os.path.join(GITHUB_DATA_DIR, 'readme_files')
METADATA_FILE = os.path.join(GITHUB_DATA_DIR, 'metadata.json')
VECTORDB_PATH = "./vector_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "my_embeddings"

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
        collection_name=COLLECTION_NAME
    )
    builder.build(chunk_size=200, chunk_overlap=200)
    print("Vector Database built successfully.")

if __name__ == "__main__":
    setup()
