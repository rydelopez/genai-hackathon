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
    avg_response_length = calculate_avg_response_length(db, conversation_id)
    unique_words = calculate_unique_words(db, conversation_id)
    response_time = calculate_response_time(db, conversation_id)
    q_and_a = fetch_q_and_a(db, conversation_id)  # This should return a list of dictionaries or objects matching the QA model

    return SecondPageStats(
        avg_response_length=avg_response_length,
        unique_words=unique_words,
        response_time=response_time,
        q_and_a=q_and_a
    )

# Placeholder functions for calculations
# Implement these functions based on your data and requirements
def calculate_avg_response_length(db: Session, conversation_id: int) -> int:
    # This is a simplified query. You need to adapt it to your actual data model.
    messages = db.query(Message).filter(Message.conversation_id == conversation_id, Message.is_response == True)
    total_length = sum(len(message.text) for message in messages)
    avg_length = total_length / messages.count() if messages.count() else 0
    return avg_length


def calculate_unique_words(db: Session, conversation_id: int) -> int:
    messages = db.query(Message).filter(Message.conversation_id == conversation_id)
    words = set()
    for message in messages:
        words.update(message.text.split())  # This simplistic split might need to be replaced with a more sophisticated tokenizer
    return len(words)


def calculate_response_time(db: Session, conversation_id: int) -> int:
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp.asc()).all()
    total_time = 0
    for i in range(1, len(messages)):
        total_time += (messages[i].timestamp - messages[i-1].timestamp).seconds
    avg_time = total_time / (len(messages) - 1) if messages else 0
    return avg_time


def fetch_q_and_a(db: Session, conversation_id: int):
    # This implementation is highly dependent on your data model.
    # Here's a conceptual approach assuming sequential Q&A.
    messages = db.query(QuestionResponse).filter(QuestionResponse.conversation_id == conversation_id).all()
    q_and_a = []
    for i in range(0, len(messages)-1, 2):  # Assuming every question is immediately followed by its answer
        q_and_a.append({"question": messages[i].text, "answer": messages[i+1].text})
    return q_and_a

