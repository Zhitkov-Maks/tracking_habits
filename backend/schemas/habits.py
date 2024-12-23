from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict


class ChangeIsActiveSchema(BaseModel):
    """A scheme for changing the activity of a habit."""

    is_active: bool = Field(..., description="True or False")


class HabitSchema(BaseModel):
    """A scheme for adding a new habit."""

    title: str = Field(
        ...,
        min_length=1,
        description="Short name of the habit"
    )
    body: str = Field(
        ...,
        min_length=1,
        description="A detailed description of the new habit. "
                    "Why, why does he want this?",
    )
    number_of_days: int = Field(
        ...,
        description="The number of days during which the user wants "
                    "to track the habit.",
    )


class FullHabitSchema(HabitSchema):
    """A scheme with all the data about the habit."""
    id: int = Field(..., description="The ID of the habit.")


class ListHabitsSchema(BaseModel):
    """A list of the user's habits."""

    data: List[FullHabitSchema] = Field(
        ...,
        description="An object with a list of habits."
    )


class AddTrackSchema(BaseModel):
    """A scheme for adding tracking to a habit."""
    done: bool = Field(
        ...,
        description="Habit tracking been completed or not completed "
                    "for a given day.",
    )
    date: datetime = None


class Tracking(BaseModel):
    """A scheme for sending data about tracking habits."""

    model_config = ConfigDict(from_attributes=True)
    done: bool = Field(
        ...,
        description="Has habit tracking been completed or not completed "
                    "for a given day.",
    )
    date: datetime = None
    habit_id: int = Field(..., description="The ID of the habit.")
    id: int = Field(..., description="The ID of the Tracking.")


class FullTracking(BaseModel):
    """The scheme for sending the tracking report."""

    done: int = Field(
        ...,
        description="The number of completed days."
    )
    not_done: int = Field(
        ...,
        description="The number of days not completed."
    )
    all: List[Tracking] = Field(
        ..., description="The report for the last week."
    )


class HabitFull(BaseModel):
    """
    A scheme with full information about the habit. Where included
    completed days and unfulfilled days.
    """

    title: str = Field(
        ...,
        min_length=1,
        description="The short name of the habit."
    )
    body: str = Field(
        ...,
        min_length=1,
        description="A detailed description of the habit. "
                    "Why, why does he want this?",
    )
    number_of_days: int = Field(
        ...,
        description="The number of days during which the user wants "
                    "to track the habit.",
    )
    start_date: datetime = None
    end_date: datetime = None
    is_active: bool = Field(..., description="True or False")
    tracking: FullTracking = Field(
        ...,
        description="An object with tracking days."
    )
