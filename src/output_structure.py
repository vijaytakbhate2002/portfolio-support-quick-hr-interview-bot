from pydantic import BaseModel, Field
from typing import Literal, Optional, Annotated, Union


class QuestionCategory(BaseModel):
    """ Question category is pydantic dictionary used to control output of question_category_model.
        output should be one word out of all literals."""
    question_category: Annotated[Union[str,
        Literal["project", "personal", "experience", "education", "soft_skills", "others"]],
        "question category represent category of question"
    ] = "other"


class InterviewResponse(BaseModel):
    """ Interview Response is pydantic dictionary used to control output of interview_model.
        response_message: It will cover llm's text response
        list_items: If there are bullet points in response then these points will added into this variable
        reference_links: This is Union of str and list of str, referred to show related links (project link etc.)"""
    response_message: Annotated[str, "Response from AI"]
    list_items: Annotated[Optional[Union[str, list[str]]], "List of items if needed to provide"] = None
    reference_links: Annotated[Optional[Union[str, list[str]]], "List out reference links associated with this response"] = None


class ValidationScores(BaseModel):
    """Each score should range from 0 to 1"""
    relevancy_score: Annotated[
        float,
        Field(ge=0, le=1, description="Relevancy of response with the actual facts provided in input prompt")
    ]
    faithfulness_score: Annotated[
        float,
        Field(ge=0, le=1, description="Faithfulness of response with the actual facts provided in input prompt")
    ]
    correctness_score: Annotated[
        float,
        Field(ge=0, le=1, description="Correctness of response with the actual facts provided in input prompt")
    ]
