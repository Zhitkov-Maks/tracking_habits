from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class AddCommentSchema(BaseModel):
    """Adding a comment to a habit."""
    body: str = Field(
        ...,
        min_length=5,
        description="A comment on a habit.",
    )


class CommentSchema(BaseModel):
    """A scheme for adding a new habit."""
    id: int = Field(..., description="The ID of the comment.")
    body: str = Field(
        ...,
        min_length=5,
        description="A comment on a habit.",
    )
    created_at: datetime = None


class ListHabitsSchema(BaseModel):
    """A list of the user's habits."""

    data: List[CommentSchema] = Field(
        ...,
        description="An object with a list of habits."
    )
