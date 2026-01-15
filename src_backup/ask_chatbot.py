from rag_assisted_bot.rag_assisted_chatbot import Assistant
GPT_MODEL_NAME = "gpt-5-mini"
VECTORDB_PATH = "./vector_db"
from dotenv import load_dotenv
load_dotenv()

assistant = Assistant(
                    gpt_model_name=GPT_MODEL_NAME,
                    vectordb_path=VECTORDB_PATH,
                    collection_name="my_embeddings",
                    temperature=0.7,
                    rag_activated=True
                    )

while True:
    question = input("You: ")
    if question == 'exit':
        break
    ai_response = assistant.chat_with_model(question)

    print("Question Category:", ai_response['question_category'])
    print("Answer -------------------------- :")
    for key, value in ai_response['response'].model_dump().items():
        print(f"{key}: {value}")
    print("\n")