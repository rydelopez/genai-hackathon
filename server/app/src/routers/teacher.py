import logging
import os

from fastapi import (
    APIRouter,
    UploadFile,
)
from celery import Celery
from app.src.schema.teacher import LessonRequest
from app.src.schema.teacher import LessonResponse
from app.src.schema.teacher import Uploads

REDIS_URL = os.environ.get("REDIS_URL")
upload_folder = "/code/shared_data"


router = APIRouter()
celery_app = Celery("main_celery_app", broker=REDIS_URL)

#create new lesson plan
@router.post("/lesson", response_model=LessonResponse)
async def create_lesson(req: LessonRequest):
    return {"lesson_id": 0}


#get uploaded docs from lesson plan
@router.get("/lesson/{lesson_id}", response_model=Uploads)
async def get_lesson(lesson_id):
    return {"uploads": []}


#delete documents from lesson plan
@router.delete("/lesson/doc/{document_id}")
async def delete_doc(document_id: int):
    #delete doc
    return {"success": 0}



#upload pdf documents to lesson plan
@router.post("/lesson/doc")
async def upload_pdf(uploaded_file: UploadFile):
    return {"success": 0}



#upload text to lesson plan
@router.post("/lesson/text")
async def upload_pdf(text: str):
    return {"success": 0}
