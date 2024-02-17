from pydantic import BaseModel

from datetime import datetime
import uuid


class Message(BaseModel):
    type: str
    contents: str

class ChatSession(BaseModel):
    message_list: list[Message] = []