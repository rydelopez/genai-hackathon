import os
from celery import Celery
from app.src.redis.config import RedisConnector
from ..redis.history import ConversationHistory

redis_connector = RedisConnector()

REDIS_URL = os.environ.get("REDIS_URL")

celery_app = Celery("main_celery_app", broker=REDIS_URL)

@celery_app.task
async def scan_database():
    redis_client = await redis_connector.create_connection()
    history = ConversationHistory(redis_client)

    await history.process_expired_conversations()


