from fastapi import FastAPI
from pydantic import BaseModel

from datetime import datetime
import uuid
from typing import List

app = FastAPI()


#model representing a lesson request
class ParentRequest(BaseModel):
    name: str
    email: str
    child_name: str
    child_age: int
    instructor_id: int



    
    