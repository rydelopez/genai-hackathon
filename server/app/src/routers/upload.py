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

@router.post("/documents/{account_id}")
async def documents(account_id):

    return {"account_id": account_id}


@router.post("/lesson/{account_id}")
async def lesson(account_id):

    return {"account_id": account_id}
