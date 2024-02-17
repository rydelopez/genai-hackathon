import os

from celery import Celery
from celery.result import AsyncResult


REDIS_URL = os.environ.get("REDIS_URL")


app = Celery("tasks", backend=REDIS_URL, broker=REDIS_URL)


@app.task
def add(x, y):
    return x + y
