from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from src.reference_data import full_resume, project, personal, experience, education, soft_skills, others
from src.output_structure import QuestionCategory, InterviewResponse
from src.prompts import question_category, conversation
from src.conversation_management import conversationUpdate
from config import GPT_MODEL_NAME
from dotenv import load_dotenv
load_dotenv()


question_category_dict = {
    'project': project,
    'personal': personal,
    'experience': experience,
    'education': education,
    'soft_skills': soft_skills,
    'other': others
}


model = ChatOpenAI(
    name=GPT_MODEL_NAME
)

conversation_model = model.with_structured_output(
    InterviewResponse,
    )

question_category_model = model.with_structured_output(
    QuestionCategory,
)

question_category_chain = question_category | question_category_model


while True:

    question = input("You: \n")
    if question == 'exit':
        break

    question_category = question_category_chain.invoke(question)
    print(question_category.question_category)

    conversation = conversationUpdate(conversation=conversation, context=question_category_dict[question_category.question_category])
    print(conversation)

    conversation.append(HumanMessage(question))
    response = conversation_model.invoke(conversation)
    print("response: ", response)
    conversation.append(AIMessage(response.response_message))




