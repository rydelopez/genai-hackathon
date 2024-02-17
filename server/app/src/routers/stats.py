import logging
import os
from datetime import datetime, timedelta
from sqlalchemy import and_

from fastapi import (
    APIRouter,
    UploadFile,
)
from celery import Celery

from app.src.schema.stats import FirstPageAggregateStats
from app.src.schema.stats import SecondPageStats
from app.models import QuestionResponse
from app.src.schema.stats import QA

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
    conversation = (
        db.query(Conversation).filter(Conversation.id == conversation_id).first()
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Example placeholders for calculating statistics
    # You need to replace these with actual data queries and calculations
    avg_response_length = conversation.average_sentences
    unique_words = conversation.unique_words
    response_time = conversation.average_response_time
    q_and_a = (
        db.query(QuestionResponse)
        .filter(QuestionResponse.conversation_id == conversation_id)
        .all()
    )
    qas = []
    for qa in q_and_a:
        qas.append(
            QA(
                question=qa.question,
                answer=qa.answer,
                ranking=qa.accuracy,
                reasoning=qa.reasoning,
            )
        )

    return SecondPageStats(
        avg_response_length=avg_response_length,
        unique_words=unique_words,
        response_time=response_time,
        q_and_a=qas,
    )

async def get_week_ago(current_time):
    return current_time - timedelta(days=7)
async def get_month_ago(current_time):
    return current_time - timedelta(days=30)
async def get_year_ago(current_time):
    return current_time - timedelta(days=365)

@router.get("/stats", response_model=FirstPageAggregateStats)
async def get_conversation_stats(parent_id, timeperiod_arg, db: Session = Depends(get_db)):
    timeperiod = timeperiod_arg or "Weekly"
    current_time = datetime.now()
    earliest = 0

    if timeperiod == "Weekly":
        earliest = get_week_ago(current_time)
    elif timeperiod == "Monthly":
        earliest = get_month_ago(current_time)
    else:
        earliest = get_year_ago(current_time)
    
    conversations = db.query(Conversation).filter(
        and_(
            Conversation.start_time >= earliest,
            Conversation.parent_id == parent_id
        )
    )

    timestamps = [conversation.start_time for conversation in conversations]
    average_sentences = [conversation.average_sentences for conversation in conversations]
    unique_words = [conversation.unique_words for conversation in conversations]
    average_response_time = [conversation.average_response_time for conversation in conversations]
    language_complexity = [conversation.language_complexity for conversation in conversations]
    sentiment = [conversation.sentiment for conversation in conversations]

    return FirstPageAggregateStats(
        timestamps,
        average_sentences,
        unique_words,
        average_response_time,
        language_complexity,
        sentiment,
    )
