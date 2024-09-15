from typing import List

from pydantic import BaseModel, ConfigDict, Field


class RemindSchema(BaseModel):
    time: int = Field(
        ...,
        description="Время(целое число от 0 до 23), для работы appscheduler"
    )



class GetRemindSchema(RemindSchema):
    model_config = ConfigDict(from_attributes=True)
    user_chat_id: int = Field(
        ...,
        description="Идентификатор пользователя телеграмм, для того "
                    "чтобы знать кому отправлять сообщение."
    )


class GetRemindSchemaAll(BaseModel):
    users: List[GetRemindSchema] = Field(
        ...,
        description="Список с пользователями у которых есть "
                    "настройка для отображения напоминаний."
    )