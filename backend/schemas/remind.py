from datetime import time

from pydantic import BaseModel, Field


class RemindSchema(BaseModel):
    user_id: int
    time: time = None