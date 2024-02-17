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
@router.post("/lesson/pdf")
async def upload_pdf_doc(uploaded_file: UploadFile, lesson_id: str):
    # Write the uploaded file to disc
    file_location = f"{upload_folder}/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    # Send a task, with the file location and project id
    celery_app.send_task(
        "app.tasks.ingest_document", args=[file_location, lesson_id], queue="vdb"
    )
    return {"filename": uploaded_file.filename}



#upload text to lesson plan
@router.post("/lesson/text")
async def upload_text_doc(text: str):
    return {"success": 0}
