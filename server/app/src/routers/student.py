import requests
import os

from celery import Celery
from fastapi import APIRouter, File, UploadFile


router = APIRouter()
upload_folder = "/code/shared_data"

REDIS_URL = os.environ.get("REDIS_URL")
celery_app = Celery("main_celery_app", broker=REDIS_URL)


@router.post("/student/chat")
async def chat(audio: UploadFile):
    file_location = f"{upload_folder}/{audio.filename}"
    file_name = audio.filename

    with open(file_location, "wb+") as file_object:
        file_object.write(audio.file.read())

    print("sending audio task to celery")

    celery_app.send_task("app.tasks.process_audio", args=[file_location, file_name], queue="celery")
    
    # You can save the file or process it as needed here
    return {"filename": audio.filename}