from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from .config import GPT_MODEL_NAME, TEMPERATURE
from .output_structure import  ValidationScores
from .prompts import  judge_model_prompt

from pydantic import BaseModel, Field
from typing import Literal, Annotated, Union
from dotenv import load_dotenv

load_dotenv()

class JudgeLLM:

    relevancy_score = []
    faithfulness_score = []
    correctness_score = []

    def __init__(self, model_name:str, temperature:float, output_structure, prompt):
        self.output_structure = output_structure
        self.prompt = prompt
        self.model_name = model_name
        self.temperature = temperature

    def buildChain(self):
        """ Create chain by using with_structured_output and return that chain """

        self.model = ChatOpenAI(
            name=self.model_name,
            temperature=self.temperature,
        )
        self.model = self.model.with_structured_output(self.output_structure)
        chain = self.prompt | self.model
        return chain

    def getScores(self):
        """ Return all scores """
        return {
            "relevancy_score": sum(self.relevancy_score) / len(self.relevancy_score),
            "faithfulness_score": sum(self.faithfulness_score) / len(self.faithfulness_score),
            "correctness_score": sum(self.correctness_score) / len(self.correctness_score)
        }

    def generateScores(self, question:str, llm_response:str, actual_fact:str):
        """ invoke the model with the given question and return its score """
        chain = self.buildChain()
        response = chain.invoke(
            {
                "question": question,
                "llm_response": llm_response,
                "actual_fact": actual_fact,
            }
        )
        self.relevancy_score.append(response.relevancy_score)
        self.faithfulness_score.append(response.faithfulness_score)
        self.correctness_score.append(response.correctness_score)



