import logging
import os
from fastapi import APIRouter, UploadFile, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from celery import Celery
# Adjust imports according to your project structure
from app.src.schema.teacher import LessonRequest, LessonResponse, Uploads
from app.models import Lesson, Document, Instructor, User, Parent  # Ensure Document is imported correctly
from app.database import SessionLocal, get_db  # Adjust the import path as necessary
from app.src.schema.parent import ParentRequest



router = APIRouter()



@router.post("/parent")
def create_parent(model: ParentRequest, db: Session = Depends(get_db)):
    # Check if the email already exists
    existing_user = db.query(User).filter(User.email == model.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if the instructor exists
    instructor = db.query(Instructor).filter(Instructor.id == model.instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    # Create a new parent instance. This also creates a User due to inheritance.
    new_parent = Parent(name=model.name, email=model.email, child_name=model.child_name, child_age=child_age, instructor_id=instructor_id, type="parent")
    db.add(new_parent)
    db.commit()
    db.refresh(new_parent)
    return new_parent


#Get a list of instrctor ids and names
@router.get("/user/{email}")
async def get_user(email, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    return user