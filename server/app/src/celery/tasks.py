import os

import json
import weaviate

from fastapi import UploadFile
from celery import Celery
from celery.result import AsyncResult
from app.src.redis.config import RedisConnector
from ..redis.history import ConversationHistory

from unstructured.partition.pdf import partition_pdf

# fix, call functions here in a new celery task
from stats import sentiment

redis_connector = RedisConnector()

REDIS_URL = os.environ.get("REDIS_URL")
WEAVIATE_URL = os.environ.get("WEAVIATE_URL")

app = Celery("celery", backend=REDIS_URL, broker=REDIS_URL)

app.conf.beat_schedule = {
    "add-every-30-seconds": {
        "task": "celery_worker.scan_database",  # Task to run
        "schedule": 600,   # Run every 30 seconds
    },
}

# Optional settings
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

@app.task
async def scan_database():
    redis_client = await redis_connector.create_connection()
    history = ConversationHistory(redis_client)

    await history.process_expired_conversations()