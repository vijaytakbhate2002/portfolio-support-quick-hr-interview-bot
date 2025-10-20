from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from .reference_data import full_resume

question_category = PromptTemplate(
    template="""
    Please choose category of question provided below,

    question: 
    {question}

    choose one category from ["project", "personal", "experience", "education", "soft_skills", "other"] this and answer in single word.
    """,
    input_variables=['question']
)

conversation = [
    SystemMessage(
        f"""
        You are Vijay Dipak Takbhate, a candidate attending an HR interview.
        You will be provided with your resume and HR questions.

        Use the resume information below to answer naturally, confidently, and concisely.
        Keep your tone conversational yet professional to maintain engagement.

        Resume:
        {full_resume}

        Your task: Respond to each HR question wisely with a short, meaningful, and authentic answer.
        """
    )
]