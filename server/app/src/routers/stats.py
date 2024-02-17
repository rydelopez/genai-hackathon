import logging
import os

from fastapi import (
    APIRouter,
    UploadFile,
)
from celery import Celery

from app.src.schema.stats import FirstPageStats
from app.src.schema.stats import SecondPageStats

REDIS_URL = os.environ.get("REDIS_URL")
upload_folder = "/code/shared_data"


router = APIRouter()
celery_app = Celery("main_celery_app", broker=REDIS_URL)


@router.get("/stats/conversation/{conversation_id}", response_model=SecondPageStats)
async def get_conversation_stats(conversation_id):
    return {"avg_response_length": 0, "unique_length": 0, "response_time": 0}


    
