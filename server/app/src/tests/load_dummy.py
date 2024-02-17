import logging
import os
from fastapi import APIRouter, UploadFile, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from celery import Celery
# Adjust imports according to your project structure
from app.src.schema.teacher import LessonRequest, LessonResponse, Uploads, InstructorResponse, InstructorRequest
from app.models import Lesson, Document, Instructor, User, Parent, Conversation  # Ensure Document is imported correctly
from app.database import SessionLocal, get_db  # Adjust the import path as necessary
from typing import List
from datetime import datetime, timedelta
import random

def load_dummy_data():
    db = SessionLocal()

    try:
        new_instructor = Instructor(name="Instructor", email="bewill@gmail.com", grade="8", type="instructor")
        db.add(new_instructor)
        db.commit()
        new_parent = Parent(name="Instructor", email="bewill2@gmail.com", child_name="bruh", child_age=4, instructor_id = new_instructor.id, type="parent")
        db.add(new_parent)
        db.commit()

        # create lesson plan
        new_lesson = Lesson(instructor_id=new_instructor.id, description="bruh")
        db.add(new_lesson)
        db.commit()

        # create 10 conversations
        for _ in range(10):
            start_time = datetime.now() - timedelta(days=random.randint(0,10))
            average_sentences = random.randint(5, 15)
            unique_words = random.randint(50, 200)
            average_response_time = random.randint(1, 60)  # assuming seconds
            language_complexity = random.randint(1, 10)
            positive = random.uniform(0, 1)
            neutral = random.uniform(0, 1 - positive)
            negative = 1 - positive - neutral

            sentiment = {
                "positive": positive,
                "neutral": neutral,
                "negative": negative
            }
            
            new_conversation = Conversation(
                parent_id=new_parent.id,
                lesson_id=new_lesson.id,
                start_time=start_time,
                average_sentences=average_sentences,
                unique_words=unique_words,
                average_response_time=average_response_time,
                language_complexity=language_complexity,
                sentiment=sentiment
            )
            db.add(new_conversation)
        
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    finally:
        db.close()