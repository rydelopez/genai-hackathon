import logging
import os
from fastapi import APIRouter, UploadFile, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from celery import Celery
# Adjust imports according to your project structure
from app.src.schema.teacher import LessonRequest, LessonResponse, Uploads
from app.models import Lesson, Document, Instructor, User, Parent  # Ensure Document is imported correctly
from app.database import SessionLocal, get_db  # Adjust the import path as necessary

REDIS_URL = os.environ.get("REDIS_URL")
upload_folder = "/code/shared_data"

router = APIRouter()
celery_app = Celery("main_celery_app", broker=REDIS_URL)


@router.post("/parent")
def create_parent(name: str, email: str, child_name: str, child_age: int, instructor_id: int, db: Session = Depends(get_db)):
    # Check if the email already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if the instructor exists
    instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    # Create a new parent instance. This also creates a User due to inheritance.
    new_parent = Parent(name=name, email=email, child_name=child_name, child_age=child_age, instructor_id=instructor_id)
    db.add(new_parent)
    db.commit()
    db.refresh(new_parent)
    return {
        "parent_id": new_parent.id
    }