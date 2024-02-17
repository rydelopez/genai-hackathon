from fastapi import FastAPI
from pydantic import BaseModel

from datetime import datetime
import uuid

app = FastAPI()


class Message(BaseModel):
    type: str
    contents: str

class ChatSession(BaseModel):
    message_list: list[Message] = []