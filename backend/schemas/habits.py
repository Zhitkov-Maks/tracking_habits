from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class HabitsSchema(BaseModel):
    title: str = Field(..., min_length=3)
    body: str =Field(..., min_length=10)
    number_of_days: int


class Habits(BaseModel):
    title: str = Field(..., min_length=3)
    body: str =Field(..., min_length=10)
    start_date: datetime = None
    is_active: bool


class ListHabitsSchema(BaseModel):
    data: List[Habits]
