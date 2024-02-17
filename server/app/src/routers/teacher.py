import logging
import os
from fastapi import APIRouter, UploadFile, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from celery import Celery
# Adjust imports according to your project structure
from app.src.schema.teacher import LessonRequest, LessonResponse, Uploads, InstructorResponse
from app.models import Lesson, Document, Instructor, User  # Ensure Document is imported correctly
from app.database import SessionLocal, get_db  # Adjust the import path as necessary
from typing import List

REDIS_URL = os.environ.get("REDIS_URL")
upload_folder = "/code/shared_data"

router = APIRouter()
celery_app = Celery("main_celery_app", broker=REDIS_URL)


@router.post("/instructor")
def create_instructor(name: str, email: str, grade: int, db: Session = Depends(get_db)):
    # Check if the email already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create a new instructor instance. This also creates a User due to inheritance.
    new_instructor = Instructor(name=name, email=email, grade=grade)
    db.add(new_instructor)
    db.commit()
    db.refresh(new_instructor)
    return {"instructor_id": new_instructor.id}


# Create new lesson plan
@router.post("/lesson", response_model=LessonResponse)
async def create_lesson(req: LessonRequest, db: Session = Depends(get_db)):
    new_lesson = Lesson(instructor_id=req.instructor_id, description=req.description)
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return {"lesson_id": new_lesson.id}


# Get uploaded docs from lesson plan
@router.get("/lesson/{lesson_id}", response_model=Uploads)
async def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    uploads = [{"name": document.name, "document_id": document.id} for document in lesson.documents]
    return {"uploads": uploads}


# Delete documents from lesson plan
@router.delete("/lesson/doc/{document_id}")
async def delete_doc(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(document)
    db.commit()
    return {"success": True}


# Upload PDF documents to lesson plan
@router.post("/lesson/pdf")
async def upload_pdf_doc(uploaded_file: UploadFile, lesson_id: int, db: Session = Depends(get_db)):
    file_location = f"{upload_folder}/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    new_document = Document(name=uploaded_file.filename, lesson_id=lesson_id)
    db.add(new_document)
    db.commit()

    celery_app.send_task("app.tasks.ingest_document", args=[file_location, str(lesson_id)], queue="vdb")
    return {"filename": uploaded_file.filename}


# Upload text to lesson plan
@router.post("/lesson/text")
async def upload_text_doc(
    text: str = Form(...),
    lesson_id: int = Form(...),
    db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    document = Document(name="Text Document", lesson_id=lesson.id)
    # Assuming Document model has a way to store the actual text. Adjust as necessary.
    db.add(document)
    db.commit()
    db.refresh(document)

    return {"success": True, "document_id": document.id}


#Get a list of instrctor ids and names
@router.get("/instructors", response_model=List[InstructorResponse])
async def get_instructors(db: Session = Depends(get_db)):
    instructors = db.query(Instructor.id, User.name).join(User, Instructor.id == User.id).all()
    return instructors