import logging
import os

from fastapi import (
    APIRouter,
    UploadFile,
)
from celery import Celery

from app.src.schema.stats import FirstPageStats
from app.src.schema.stats import SecondPageStats
from app.models import QuestionResponse

REDIS_URL = os.environ.get("REDIS_URL")
upload_folder = "/code/shared_data"

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db  # Ensure this import matches your project structure
from app.models import Conversation  # Adjust imports based on your actual models

router = APIRouter()

@router.get("/stats/conversation/{conversation_id}", response_model=SecondPageStats)
async def get_conversation_stats(conversation_id: int, db: Session = Depends(get_db)):
    # Fetch the conversation by ID to ensure it exists
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Example placeholders for calculating statistics
    # You need to replace these with actual data queries and calculations
    avg_response_length = conversation.average_sentences
    unique_words = conversation.unique_words
    response_time = conversation.average_response_time
    q_and_a = db.query(QuestionResponse).filter(QuestionResponse.id == conversation_id).all()

    return SecondPageStats(
        avg_response_length=avg_response_length,
        unique_words=unique_words,
        response_time=response_time,
        q_and_a=q_and_a
    )


