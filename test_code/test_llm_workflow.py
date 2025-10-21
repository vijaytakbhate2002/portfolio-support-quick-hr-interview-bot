import os
import sys
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
sys.path.extend([SRC_PATH, PROJECT_ROOT])

from src.llm_judge import JudgeLLM
from src.config import GPT_MODEL_NAME
from src.output_structure import InterviewResponse, QuestionCategory, ValidationScores
from src.prompts import question_category_prompt, judge_model_prompt
from main import ResumeAssistant


@pytest.fixture(scope="module")
def assistant():
    return ResumeAssistant(
        model_name=GPT_MODEL_NAME,
        temperature=0.5,
        conversation_structure=InterviewResponse,
        question_category_structure=QuestionCategory,
        question_category_prompt=question_category_prompt
    )


@pytest.fixture(scope="module")
def judge():
    return JudgeLLM(
        output_structure=ValidationScores,
        prompt=judge_model_prompt
    )


test_question = "What challenges did you face in your last project, and how did you overcome them?"


def test_question_category_model(assistant):
    response = assistant.chatWithModel(question=test_question)

    assert isinstance(response, dict), "Response must be a dictionary."
    assert 'question_category' in response, "Missing 'question_category' key."
    assert 'response' in response, "Missing 'response' key."

    category = response['question_category'].lower()
    assert "project" in category, f"Expected category 'project' but got '{category}'"


def test_validation_pipeline(assistant, judge):
    response = assistant.chatWithModel(question=test_question)

    judge.generateScores(
        question=test_question,
        llm_response=response['response'].response_message,
        actual_fact=assistant.question_category_dict[response['question_category']]
    )

    assert hasattr(judge, 'relevancy_score')
    assert hasattr(judge, 'faithfulness_score')
    assert hasattr(judge, 'correctness_score')

    assert 0 <= judge.relevancy_score[0] <= 1
    assert 0 <= judge.faithfulness_score[0] <= 1
    assert 0 <= judge.correctness_score[0] <= 1
