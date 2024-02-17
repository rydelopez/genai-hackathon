import os

import json
from server.app.src.celery.complexity import measure_convo_complexity
from server.app.src.celery.sentiment import measure_convo_sentiment
from server.app.src.celery.topics import measure_convo_topics
import weaviate

from fastapi import UploadFile, Depends
from celery import Celery
from celery.result import AsyncResult
from app.src.redis.config import RedisConnector
from ..redis.history import ConversationHistory
from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db
from app.models import Conversation, QuestionResponse, ConversationConceptFocus, Parent, Lesson

from unstructured.partition.pdf import partition_pdf

# fix, call functions here in a new celery task
from stats import sentiment

redis_connector = RedisConnector()

REDIS_URL = os.environ.get("REDIS_URL")
WEAVIATE_URL = os.environ.get("WEAVIATE_URL")

app = Celery("celery", backend=REDIS_URL, broker=REDIS_URL)

# Beat Scheduler Settings
app.conf.beat_schedule = {
    "add-every-30-seconds": {
        "task": "celery_worker.scan_database",
        "schedule": 600,
    },
}
app.conf.timezone = 'UTC'


@app.task()
def ingest_document(file_path: str, project_id: str):
    # Open the downloaded file and get the elements
    elements = partition_pdf(filename=file_path)
    document_text = " ".join(e.text for e in elements)
    print("processed document")

    # Upload to Weaviate
    item = {"source": file_path, "content": document_text, "project_id": project_id}
    client = weaviate.Client(
        url=WEAVIATE_URL,
    )

    client.batch.configure(batch_size=1)  # Configure batch
    with client.batch as batch:
        batch.add_data_object(item, "Document")
    print("embedded and added document to vdb")

    return "Completed document ingest."

@app.task()
def add_conversation_metadata(parent_id, metadata, db: Session = Depends(get_db)):
    instructor_id = db.query(Parent).filter(Parent.id == parent_id).first().instructor_id
    lesson_id = db.query(Lesson).filter(Lesson.instructor_id == instructor_id).order_by(Lesson.time.desc()).first().id

    num_questions = metadata["num_questions"]
    average_sentences = int(metadata["num_sentences"] / num_questions)
    average_response_time = int(metadata["total_response_time"] / num_questions)
    
    new_conversation = Conversation(
        parent_id=parent_id,
        lesson_id=lesson_id,
        average_sentences=average_sentences,
        unique_words=metadata["num_unique_words"],
        average_response_time=average_response_time
    )
    db.add(new_conversation)
    db.commit()

    return new_conversation.id

@app.task()
def calculate_nlp_metrics(conversation_id, messages, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()

    # calculate conversation fields
    conversation.language_complexity = int(measure_convo_complexity(messages)["avg_complexity"] * 100)
    conversation.sentiment = measure_convo_sentiment(messages)
    db.commit()

    # calculate topic fields
    concept_counter = measure_convo_topics(messages)
    total_messages = sum(concept_counter.values())
    for concept_id, freq in concept_counter.items():
        new_concept_focus = ConversationConceptFocus(conversation_id=conversation_id, concept_id=concept_id, percentage=int(100 * 1.0 * freq / total_messages))
        db.add(new_concept_focus)
    db.commit()
    
    # LATER: calculate accuracy metrics

@app.task()
def add_conversation_to_db(conversation_id, question_answers, db: Session = Depends(get_db)):
    objs = [QuestionResponse(
        conversation_id=conversation_id,
        question=qa["question"],
        answer=qa["answer"]
    ) for qa in question_answers]
    db.add_all(objs)
    db.commit()

@app.task
async def scan_database():
    redis_client = await redis_connector.create_connection()
    history = ConversationHistory(redis_client)

    await history.process_expired_conversations()