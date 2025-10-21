from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from .reference_data import full_resume

question_category_prompt = PromptTemplate(
    template="""
    Please choose category of question provided below,

    question: 
    {question}

    choose one category from ["project", "personal", "experience", "education", "soft_skills", "other"] this and answer in single word.
    """,
    input_variables=['question']
)

conversation_prompt = [
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

judge_model_prompt = PromptTemplate(
    template="""
    I will give you question asked by HR and answer given by the llm, your task is to generate following scores by comparing llm output with actual fact that is provided

    Scores types:
    relevancy_score, faithfulness_score, correctness_score

    question asked:
    {question}

    llm response:
    {llm_response}

    actual fact:
    {actual_fact}

    generate each score ranging from 0 to 1 (float)
    """,
    input_variables=['question', 'llm_response', 'actual_fact']
)
