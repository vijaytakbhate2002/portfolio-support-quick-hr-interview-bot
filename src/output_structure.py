from pydantic import BaseModel
from typing import Literal, Optional, Annotated, Union


class QuestionCategory(BaseModel):
    question_category: Annotated[Union[str,
        Literal["project", "personal", "experience", "education", "soft_skills", "others"]],
        "question category represent category of question"
    ] = "other"


class InterviewResponse(BaseModel):
    response_message: Annotated[str, "Response from AI"]
    list_items: Annotated[Optional[Union[str, list[str]]], "List of items if needed to provide"] = None
    reference_links: Annotated[Optional[Union[str, list[str]]], "List out reference links associated with this response"] = None
