from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict


class ChangeIsActiveSchema(BaseModel):
    """Схема для изменения активности привычки."""
    is_active: bool = Field(..., description="True или False")



class HabitSchema(BaseModel):
    """Схема для добавления новой привычки для отслеживания."""
    title: str = Field(
        ..., min_length=3, description="Краткое название привычки"
    )
    body: str =Field(
        ...,
        min_length=10,
        description="Подробное описание, что вы хотите сделать пользователь и "
                    "с какой целью."
    )
    number_of_days: int = Field(
        ...,
        description="Количество дней, в течении которых пользователь "
                    "хочет отслеживать привычку."
    )


class FullHabitSchema(HabitSchema):
    id: int = Field(..., description="ID habit's")


class ListHabitsSchema(BaseModel):
    """Список активных привычек пользователя."""
    data: List[FullHabitSchema] = Field(
        ..., description="Объект со списком привычек."
    )


class AddTrackSchema(BaseModel):
    done: bool = Field(
        ...,
        description="Выполнено или не выполнено "
                    "отслеживание привычки за какой-то день."
    )
    date: datetime = None


class Tracking(BaseModel):
    """Схема для отправки данных об отслеживании привычки."""
    model_config = ConfigDict(from_attributes=True)
    done: bool = Field(
        ...,
        description="Выполнено или не выполнено "
                    "отслеживание привычки за какой-то день."
    )
    date: datetime = None
    habit_id: int = Field(..., description="ID привычки")
    id: int = Field(..., description="ID tracking")


class FullTracking(BaseModel):
    """
    Схема для отправки отслеживаний с выполненными датами и невыполненными.
    """
    done: List[Tracking] = Field(
        ..., description="Список с выполненными днями."
    )
    not_done: List[Tracking] = Field(
        ..., description="Список с не выполненными днями."
    )
    all: List[Tracking] = Field(
        ..., description="Список с не выполненными днями."
    )


class HabitFull(BaseModel):
    """
    Схема с полной информацией о привычке. Куда входят
    выполненные дни и невыполненные дни.
    """
    title: str = Field(
        ..., min_length=3, description="Краткое название привычки"
    )
    body: str =Field(
        ...,
        min_length=10,
        description="Подробное описание, что вы хотите сделать пользователь и "
                    "с какой целью."
    )
    number_of_days: int = Field(
        ...,
        description="Количество дней, в течении которых пользователь "
                    "хочет отслеживать привычку."
    )
    start_date: datetime = None
    end_date: datetime = None
    is_active: bool
    tracking: FullTracking = Field(
        ...,
        description="Объект с отслеживанием дней."
    )
