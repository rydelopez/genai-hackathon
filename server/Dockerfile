FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/server/
COPY ./requirements.txt /code/server/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/server/requirements.txt

COPY ./app /code/server/app

CMD ["uvicorn", "app.main:api", "--host", "0.0.0.0", "--port", "3500", "--reload"]