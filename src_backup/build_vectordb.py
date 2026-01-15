VECTORDB_PATH = "./vector_db"
from dotenv import load_dotenv
from rag_assisted_bot.rag_assisted_chatbot import BuildVectorDB

load_dotenv()

builder = BuildVectorDB(
    directory_path='./github_data/readme_files',
    vectordb_path=VECTORDB_PATH,
    embedding_model_name="all-MiniLM-L6-v2",
    collection_name="my_embeddings"
)
builder.build(chunk_size=200, chunk_overlap=200)