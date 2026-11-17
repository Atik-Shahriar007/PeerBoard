
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import User, Question, Answer


# Application startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# Request model for creating users
class UserCreate(BaseModel):
    name: str
    email: str


# Request model for creating/updating questions
class QuestionCreate(BaseModel):
    title: str
    body: str
    course_code: str
    tags: list[str] = Field(default_factory=list)
    author_id: int


@app.post("/users", response_model=User, status_code=201)
def create_user(
    data: UserCreate,
    session: Session = Depends(get_session)
):

    user = User(
        name=data.name,
        email=data.email
    )

    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    session.refresh(user)

    return user


@app.post("/questions", response_model=Question, status_code=201)
def create_question(
    data: QuestionCreate,
    session: Session = Depends(get_session)
):

    # Check whether the author exists
    author = session.get(User, data.author_id)

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    # Validate title and body
    if not data.title.strip() or not data.body.strip():
        raise HTTPException(
            status_code=400,
            detail="Title and body cannot be blank"
        )

    # Create question
    question = Question(
        **data.model_dump(),
        accepted_answer_id=None
    )

    session.add(question)
    session.commit()
    session.refresh(question)

    return question



@app.get("/questions", response_model=list[Question])
def list_questions(
    session: Session = Depends(get_session)
):

    questions = session.exec(
        select(Question)
    ).all()

    return questions



@app.get("/questions/{question_id}", response_model=Question)
def get_question(
    question_id: int,
    session: Session = Depends(get_session)
):

    question = session.get(Question, question_id)

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    return question


@app.put("/questions/{question_id}", response_model=Question)
def update_question(
    question_id: int,
    data: QuestionCreate,
    session: Session = Depends(get_session)
):

    question = session.get(Question, question_id)

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    # Check whether the new author exists
    author = session.get(User, data.author_id)

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    # Validate title and body
    if not data.title.strip() or not data.body.strip():
        raise HTTPException(
            status_code=400,
            detail="Title and body cannot be blank"
        )

    # Update question fields
    question.title = data.title
    question.body = data.body
    question.course_code = data.course_code
    question.tags = data.tags
    question.author_id = data.author_id

    question.updated_at = datetime.now(timezone.utc)

    session.add(question)
    session.commit()
    session.refresh(question)

    return question


@app.delete("/questions/{question_id}")
def delete_question(
    question_id: int,
    session: Session = Depends(get_session)
):

    question = session.get(Question, question_id)

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    # Check whether the question has answers
    existing_answer = session.exec(
        select(Answer).where(
            Answer.question_id == question_id
        )
    ).first()

    if existing_answer:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete a question with existing answers"
        )

    session.delete(question)
    session.commit()

    return {"message": "Question deleted"}
