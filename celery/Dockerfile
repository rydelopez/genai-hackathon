FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/celery
COPY ./requirements.txt /code/celery/requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir --upgrade -r /code/celery/requirements.txt

COPY ./app /code/celery/app

CMD ["celery", "-A", "app.tasks", "worker", "-Q", "celery", "--loglevel=info"]