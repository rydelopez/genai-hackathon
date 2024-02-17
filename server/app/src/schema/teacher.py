from fastapi import FastAPI
from pydantic import BaseModel

from datetime import datetime
import uuid
from typing import List

app = FastAPI()


#model representing a lesson request
class LessonRequest(BaseModel):
    instructor_id: int #id of teacher creating the lesson
    description: str  #descipriton of lesson
    concepts: List[str] #concepts 

#model representing a lesson request
class LessonResponse(BaseModel):
    lesson_id: int  #lesson_id of created lesson

#model representing an Uploaded doc
class Upload(BaseModel):
    document_id: int
    name: str

#model representing response for uploaded docs
class Uploads(BaseModel):
    uploads: List[Upload]

#model representing response for uploaded docs
class InstructorResponse(BaseModel):
    instructor_id: int
    name: str


    
    