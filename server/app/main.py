from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


import uvicorn
import os

from fastapi import FastAPI, Request
from celery import Celery

from app.src.routers import conversation
from app.src.routers import stats


REDIS_URL = os.environ.get("REDIS_URL")


app = FastAPI()
app.include_router(conversation.router)
app.include_router(stats.router)

# Create the celery instance
celery_app = Celery("main_celery_app", broker=REDIS_URL)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Base route
@app.get("/")
async def root():
    return {"msg": "API is Online!"}


if __name__ == "__main__":
    if os.environ.get("APP_ENV") == "development":
        uvicorn.run("app.main:app", host="0.0.0.0", port=3500, workers=4, reload=True)
    else:
        pass
