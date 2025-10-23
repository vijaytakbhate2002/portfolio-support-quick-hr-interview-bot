from src.llm_judge import JudgeLLM
from src.config import GPT_MODEL_NAME, MLFLOW_TRACKING_URI, TEMPERATURE
from src.output_structure import InterviewResponse, QuestionCategory, ValidationScores
from src.prompts import question_category_prompt, judge_model_prompt
from src.reference_data import test_questions
from main import ResumeAssistant
import mlflow
from mlflow import log_metric, log_param, log_metrics
import json

assistant = ResumeAssistant(
        model_name=GPT_MODEL_NAME,
        temperature=0.5,
        conversation_structure=InterviewResponse,
        question_category_structure=QuestionCategory,
        question_category_prompt=question_category_prompt

    )

judge = JudgeLLM(
    output_structure=ValidationScores,
    prompt=judge_model_prompt,
    model_name=GPT_MODEL_NAME,
    temperature=TEMPERATURE,
)

for question in test_questions:
    print(question)
    response = assistant.chatWithModel(question=question)
    judge.generateScores(question=question,
                   llm_response=response['response'].response_message,
                   actual_fact=assistant.question_category_dict[response['question_category']])

    print(response)
    print(judge.getScores())



mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

experiment_name = "LLM_Response_Validation"
mlflow.set_experiment(experiment_name)

with mlflow.start_run(run_name="Run_2"):
    log_param("model_name", "gpt-5-mini")
    log_param("data_source", "Resume Sections")
    log_param("temperature", TEMPERATURE)

    log_metrics(judge.getScores())

    with open("response_example.json", "w") as f:
        json.dump({
            "question": question,
            "question_category": response["question_category"],
            "response": response["response"].model_dump()
        }, f, indent=2)

    mlflow.log_artifacts("response_example.json")

    print("MLflow run logged successfully!")


