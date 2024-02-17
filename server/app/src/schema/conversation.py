from fastapi import FastAPI
from pydantic import BaseModel

from datetime import datetime
import uuid

app = FastAPI()


class Message(BaseModel):
    conversation_id: str | None = "1"
    project_id: str
    name: str | None = None
    message: str | None = None
    time_stamp: datetime | None = None


class ChatSession(BaseModel):
    message_list: list[Message] = []
    session_id: uuid.UUID
    user_id: uuid.UUID
    project_id: uuid.UUID
    last_time_used: datetime | None = None
