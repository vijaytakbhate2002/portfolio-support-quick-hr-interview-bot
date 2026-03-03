from rag_assisted_bots import Assistant
from dotenv import load_dotenv
import os
import time

load_dotenv()

# RAG Configuration
VECTORDB_PATH = "./medium_vector_db"
COLLECTION_NAME = "my_embeddings"

# Initialize the new RAG Assistant
assistant = Assistant(
    gpt_model_name="gpt-5-mini",
    vectordb_path=VECTORDB_PATH, 
    collection_name=COLLECTION_NAME,
    temperature=0.7,
    rag_activated=True,
    assistant_type="medium"
)

while True:
    question = input("Enter your question (or 'exit' to quit): ")
    if question.lower() == 'exit':
        print("Exiting the chatbot. Goodbye!")
        break
    # time the response generation    start_time = time.time()
    start_time = time.time()
    result = assistant.chat_with_model(question = question)
    end_time = time.time()
    
    print(f"Response generated in {end_time - start_time:.2f} seconds")

    print("Response:", result["response"])
    print("RAG relevance:", result["rag_relevance"])
    print("Metadatas:", result["metadatas"])
    print("RAG Context:", result["rag_context"])

    