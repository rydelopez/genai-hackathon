import logging
import os

from fastapi import (
    APIRouter,
    UploadFile,
)
from celery import Celery


REDIS_URL = os.environ.get("REDIS_URL")
upload_folder = "/code/shared_data"


router = APIRouter()
celery_app = Celery("main_celery_app", broker=REDIS_URL)


@router.post("/ingestdoc")
async def ingest_document(uploaded_file: UploadFile, project_id: str):
    # Write the uploaded file to disc
    file_location = f"{upload_folder}/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    # Send a task, with the file location and project id
    celery_app.send_task(
        "app.tasks.ingest_document", args=[file_location, project_id], queue="vdb"
    )
    return {"filename": uploaded_file.filename}
