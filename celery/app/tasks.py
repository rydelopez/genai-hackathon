import os
import json

from fastapi import UploadFile

from celery import Celery
from celery.result import AsyncResult

from unstructured.partition.pdf import partition_pdf
import whisper
import weaviate


# fix, call functions here in a new celery task
from stats import sentiment

upload_folder = "/code/shared_data"

REDIS_URL = os.environ.get("REDIS_URL")
WEAVIATE_URL = os.environ.get("WEAVIATE_URL")

app = Celery("app", backend=REDIS_URL, broker=REDIS_URL)


@app.task()
def ingest_document(file_path: str, lesson_id: str):
    # Open the downloaded file and get the elements
    elements = partition_pdf(filename=file_path)
    document_text = " ".join(e.text for e in elements)
    print("Processed lesson document")

    # Upload to Weaviate
    item = {"source": file_path, "content": document_text, "lesson_id": lesson_id}
    client = weaviate.Client(
        url=WEAVIATE_URL,
    )

    client.batch.configure(batch_size=1)  # Configure batch
    with client.batch as batch:
        batch.add_data_object(item, "Document")
    print("embedded and added document to vdb")

    return "Completed document ingest."

@app.task()
def process_audio(file_path: str, file_name: str):
    print("processing audio")

    original_file_path = file_path
    mp3_file_path = f"{upload_folder}/{file_name.split('.', 1)[0]}.mp3"

    print(f"converting {original_file_path} to {mp3_file_path}")
    transcription_file_path = f"{upload_folder}/{file_name.split('.', 1)[0]}.txt"

    # Convert to mp3
    import ffmpeg

    try:
        (
            ffmpeg
            .input(original_file_path)
            .output(mp3_file_path)
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
        raise e 


    # Transcribe with whisper
    whisper_model = whisper.load_model("tiny.en")

    print(f"Transcribing {mp3_file_path}")
    result = whisper_model.transcribe(mp3_file_path)
    transcription = result["text"]
    print(f"Transcription: {transcription}")

    # Update chat history + query chatbot
    

    # get response
    

    return {'status': 'success'}