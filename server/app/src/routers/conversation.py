import logging
from pydantic import BaseModel

from uuid import uuid4

from fastapi.responses import StreamingResponse

import asyncio

from fastapi import (
    APIRouter,
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
)

from app.src.socket.connection import ConnectionManager
from app.src.redis.config import RedisConnector
from app.src.redis.consumer import Consumer
from app.src.redis.producer import Producer
from app.src.schema.conversation import Message


router = APIRouter()
connection_manager = ConnectionManager()
redis_connector = RedisConnector()


@router.post("/chatbot")
async def chatbot(
    client_message: Message,
):

    # Connect to the redis client, which we need for the producer and consumer
    redis_client = await redis_connector.create_connection()

    # Set up our consumer and consumer
    producer = Producer(redis_client)

    # Loop where we wait for a user message and send one back
    try:
        # Format message to be used by the producer
        # - Expected format: {conversation_id: message}
        # - The message id will automatically be created in `producer.py`
        message = {client_message.conversation_id: client_message.message}

        # Send message via the producer
        await producer.add_to_stream(message)
        print("Added human message to stream...")

    except Exception as e:
        print("bro An exception occurred while trying to add new message to stream")
        print(e)


@router.get("/get_messages")
async def message_stream(conversation_id: str):
    redis_client = await redis_connector.create_connection()
    consumer = Consumer(redis_client)

    return StreamingResponse(
        consumer.get_message_stream(block=0, conversation_id=conversation_id),
        media_type="text/event-stream",
    )


@router.post("/clear_history")
async def clear_history(conversation_id: str):
    redis_client = await redis_connector.create_connection()

    redis_key = f"conversation:{conversation_id}"
    await redis_client.delete(redis_key)
    return {"response": "success"}


@router.get("/get_conversation_id")
async def get_conversation_id():
    new_id = uuid4()
    return {"conversation_id": new_id.hex}
