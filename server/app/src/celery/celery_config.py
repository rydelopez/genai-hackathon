import os
from celery.schedules import crontab
from celery import Celery

REDIS_URL = os.environ.get("REDIS_URL")

celery_app = Celery("main_celery_app", broker=REDIS_URL)

# Example of a task that runs every minute
celery_app.conf.beat_schedule = {
    "add-every-30-seconds": {
        "task": "celery_worker.scan_database",  # Task to run
        "schedule": 600,   # Run every 30 seconds
    },
}

# Optional settings
celery_app.conf.timezone = 'UTC'
