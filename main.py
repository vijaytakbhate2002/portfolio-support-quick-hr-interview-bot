from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from src.reference_data import project, personal, experience, education, soft_skills, others
from src.output_structure import QuestionCategory, InterviewResponse
from src.prompts import question_category_prompt, conversation_prompt
from src.conversation_management import conversationUpdate
from src.config import GPT_MODEL_NAME
from dotenv import load_dotenv
load_dotenv()


class ResumeAssistant:

    question_category_dict = {
        'project': project,
        'personal': personal,
        'experience': experience,
        'education': education,
        'soft_skills': soft_skills,
        'other': others
    }

    conversation = conversation_prompt

    def __init__(self, model_name, temperature: float, conversation_structure, question_category_structure, question_category_prompt):
        self.model_name = model_name
        self.temperature = temperature
        self.model = ChatOpenAI(
            name=GPT_MODEL_NAME,
            temperature=temperature
        )
        self.conversation_structure = conversation_structure
        self.question_category_structure = question_category_structure
        self.question_category_prompt = question_category_prompt


    def loadModels(self):
        """ Add with structured output feature to conversation and question category model and return tuple
            Args:
                conversation_structure: Pydantic dictionary / class for conversation model output structure
                question_category_structure: Pydantic dictionary / class for question category model output structure

            Returns:
                    tuple(ChatOpenAI, ChatOpenAI)"""
        conversation_model = self.model.with_structured_output(
            self.conversation_structure,
        )

        question_category_model = self.model.with_structured_output(
            self.question_category_structure,
        )

        return conversation_model, question_category_model


    def buildChain(self, model:ChatOpenAI):
        """ Builds question category chain and conversation chain
            Args:
                prompt_template: PromptTemplate object used for model
                model: ChatOpenAI model

            Returns:
                    Returns chain"""

        chain = self.question_category_prompt | model

        return chain


    def getReadyModels(self):

        """ Create chains from model and prompts and return these chains to invoke """

        conversation_model, question_category_model = self.loadModels()
        question_category_chain = self.buildChain(question_category_model)

        return conversation_model, question_category_chain


    def chatWithModel(self, question:str) -> tuple:
        """ Takes input question and return answer of that question with updating conversation list.
            conversation list used to make model remember last 4 conversation messages
            Args:
                question: input question

            Returns:
                    (answer, question_category): returns the response of llm """

        conversation_model, question_category_chain = self.getReadyModels()
        question_category = question_category_chain.invoke(question)

        self.conversation = conversationUpdate(conversation=self.conversation,
                                          context=self.question_category_dict[question_category.question_category])

        # print(self.conversation[0])

        self.conversation.append(HumanMessage(question))
        response = conversation_model.invoke(self.conversation)
        self.conversation.append(AIMessage(response.response_message))

        return {
                "response":response,
                "question_category":question_category.question_category
        }


if __name__ == "__main__":
    assistant = ResumeAssistant(
        model_name=GPT_MODEL_NAME,
        temperature=0.5,
        conversation_structure=InterviewResponse,
        question_category_structure=QuestionCategory,
        question_category_prompt=question_category_prompt

    )

    while True:
        response = assistant.chatWithModel(question:=input("You: \n"))
        print(response)