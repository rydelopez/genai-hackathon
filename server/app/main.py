from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


import uvicorn
import os

from fastapi import FastAPI, Request
from celery import Celery

from . import models
from app.database import SessionLocal, engine
from app.src.routers import conversation, parent, stats, teacher, student
from app.src.redis.config import RedisConnector

OPENAI_API_KEY = os.environ.get("OPENAI_KEY")


REDIS_URL = os.environ.get("REDIS_URL")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

# Middleware first
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(conversation.router)
app.include_router(stats.router)
app.include_router(teacher.router)
app.include_router(parent.router)
app.include_router(student.router)

# Load In Stopwords
redis_connector = RedisConnector()
redis_client = redis_connector.create_connection()
stopwords_key = "stopwords"
with open("stopwords.txt", "r") as file:
    for line in file.readlines():
        redis_client.sadd(stopwords_key, line.strip())

# Celery
celery_app = Celery("main_celery_app", broker=REDIS_URL)

# Base route
@app.get("/")
async def root():
    return {"msg": "API is Online!"}


if __name__ == "__main__":
    if os.environ.get("APP_ENV") == "development":
        uvicorn.run("app.main:app", host="0.0.0.0", port=3500, workers=4, reload=True)
    else:
        pass
