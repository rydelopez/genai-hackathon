from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, PickleType
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    type = Column(String)

class Parent(User):
    __tablename__ = "parents"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    child_name = Column(String)
    child_age = Column(Integer)
    instructor_id = Column(Integer, ForeignKey("instructors.id"))

    conversations = relationship("Conversation", backref="parent")

class Instructor(User):
    __tablename__ = "instructors"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    grade = Column(Integer)

    lessons = relationship("Lesson", backref="instructor")
    students = relationship("Parent", backref="instructor", primaryjoin=id==Parent.instructor_id)

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    instructor_id = Column(Integer, ForeignKey("instructors.id"))
    description = Column(String)

    concepts = relationship("Concept", backref="lesson")
    documents = relationship("Document", backref="lesson")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parents.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    start_time = Column(DateTime)
    average_sentences = Column(Integer)
    unique_words = Column(Integer)
    average_response_time = Column(Integer)

    language_complexity = Column(Integer)
    sentiment = Column(PickleType)

    concept_focuses = relationship("ConversationConceptFocus", backref="conversation")
    questions = relationship("QuestionResponse", backref="conversation")

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    concepts = relationship("Concept", backref="subject")

class Concept(Base):
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))

class ConversationConceptFocus(Base):
    __tablename__ = "conversationconceptfocuses"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    concept_id = Column(Integer, ForeignKey("concepts.id"))
    percentage = Column(Integer)

class QuestionResponse(Base):
    __tablename__ = "questionresponses"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    concept_id = Column(Integer, ForeignKey("concepts.id"))
    accuracy = Column(Integer)
    reasoning = Column(String)

# NOTE: might need to define relationship from concept to conversationconceptfocuses and questionresponses

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
