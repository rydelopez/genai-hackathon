FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/vdb
COPY ./requirements.txt /code/vdb/requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir --upgrade -r /code/vdb/requirements.txt

COPY ./app /code/vdb/app

CMD ["celery", "-A", "app.tasks", "worker", "-Q", "vdb", "--loglevel=info"]