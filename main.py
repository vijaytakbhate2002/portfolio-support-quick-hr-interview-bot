from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from reference_data import context, test_context, hr_questions
from dotenv import load_dotenv
import numpy as np

load_dotenv()

model = ChatOpenAI(
    name='gpt-5-mini'
)


conversation = [
    SystemMessage(
        f"""
        You are Vijay Dipak Takbhate, a candidate attending an HR interview.
        You will be provided with your resume and HR questions.

        Use the resume information below to answer naturally, confidently, and concisely.
        Keep your tone conversational yet professional to maintain engagement.

        Resume:
        {context}

        Your task: Respond to each HR question wisely with a short, meaningful, and authentic answer.
        """
    )
]


output_parser = StrOutputParser()

chain = model | output_parser

while True:

    if len(conversation) > 4:
        print("Conversation compressed ...")
        conversation = [conversation[0]] + conversation[-4:]
        # print("After compression ", conversation)

    question = input("You: \n")
    if question == 'exit':
        break

    conversation.append(HumanMessage(question))
    response = chain.invoke(conversation)
    conversation.append(AIMessage(response))
    print("response: ", response)




