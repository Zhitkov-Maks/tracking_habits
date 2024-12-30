from typing import List

from pydantic import BaseModel, ConfigDict, Field


class RemindSchema(BaseModel):
    """A scheme for getting the time and the chat id for creating a reminder."""
    time: int = Field(
        ...,
        description="Time(integer from 0 to 23) for the appscheduler to work"
    )
    user_chat_id: int = Field(..., description="Telegram user ID")



class GetRemindSchema(RemindSchema):
    """A scheme to use as an object when receiving a list of reminders."""
    model_config = ConfigDict(from_attributes=True)
    user_chat_id: int = Field(
        ...,
        description="The telegram user's ID, in order to know who "
                    "to send the message to."
    )


class GetRemindSchemaAll(BaseModel):
    """A scheme for returning a list of users who have a reminder set up."""
    users: List[GetRemindSchema] = Field(
        ...,
        description="A list with users who have a setting for "
                    "displaying reminders."
    )
