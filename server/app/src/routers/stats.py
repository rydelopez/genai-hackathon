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


@router.get("/stats/{account_id}")
async def stats(account_id):

    return {"account_id": account_id}


@router.get("/stats/{account_id}/summary")
async def stats_summary(account_id):

    return {"account_id": account_id}


@router.get("/stats/{account_id}/history")
async def stats_history(account_id):

    return {"account_id": account_id}


@router.post("/stats/{account_id}/documents")
async def stats_documents(account_id):

    return {"account_id": account_id}

    
