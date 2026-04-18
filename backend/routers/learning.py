from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from database import get_db
from models import (
    LearningContent, Quiz, QuizQuestion, QuizAttempt, User, Student,
    UserRole, LearningContentType, QuizCorrectOption
)
from schemas import (
    LearningContentCreate, LearningContentOut,
    QuizCreate, QuizOut, QuizQuestionOut,
    QuizAttemptSubmit, QuizAttemptOut
)
from routers.auth import get_current_user

router = APIRouter(prefix="/learning", tags=["learning"])


def _content_payload(content: LearningContent, created_by_name: Optional[str] = None):
    return {
        "id": content.id,
        "title": content.title,
        "subject": content.subject,
        "grade_level": content.grade_level,
        "content_type": content.content_type,
        "url": content.url,
        "body": content.body,
        "dept_id": content.dept_id,
        "created_by": content.created_by,
        "created_by_name": created_by_name,
        "created_at": content.created_at,
    }


@router.get("", response_model=List[LearningContentOut])
async def list_learning_content(
    db: AsyncSession = Depends(get_db),
    subject: Optional[str] = Query(None),
    grade_level: Optional[int] = Query(None),
    content_type: Optional[LearningContentType] = Query(None),
):
    query = select(LearningContent)
    if subject:
        query = query.where(LearningContent.subject.ilike(f"%{subject}%"))
    if grade_level:
        query = query.where(LearningContent.grade_level == grade_level)
    if content_type:
        query = query.where(LearningContent.content_type == content_type)
    result = await db.execute(query.order_by(LearningContent.created_at.desc()))
    contents = result.scalars().all()
    creator_ids = {c.created_by for c in contents}
    creators = {}
    if creator_ids:
        user_result = await db.execute(select(User).where(User.id.in_(creator_ids)))
        creators = {u.id: u.name for u in user_result.scalars().all()}
    return [_content_payload(content, creators.get(content.created_by)) for content in contents]


@router.post("", response_model=LearningContentOut)
async def create_learning_content(
    payload: LearningContentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    content = LearningContent(
        title=payload.title,
        subject=payload.subject,
        grade_level=payload.grade_level,
        content_type=payload.content_type,
        url=payload.url,
        body=payload.body,
        created_by=current_user.id,
        dept_id=payload.dept_id,
    )
    db.add(content)
    await db.commit()
    await db.refresh(content)
    return _content_payload(content, current_user.name)


@router.get("/{id}", response_model=LearningContentOut)
async def get_learning_content(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LearningContent).where(LearningContent.id == id))
    content = result.scalars().first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    creator_result = await db.execute(select(User).where(User.id == content.created_by))
    creator = creator_result.scalars().first()
    return _content_payload(content, creator.name if creator else None)


@router.delete("/{id}")
async def delete_learning_content(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    result = await db.execute(select(LearningContent).where(LearningContent.id == id))
    content = result.scalars().first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    if current_user.role == UserRole.faculty and content.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own content")
    await db.delete(content)
    await db.commit()
    return {"message": "Content deleted"}


@router.get("/{id}/quiz", response_model=Optional[QuizOut])
async def get_quiz_for_content(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LearningContent).where(LearningContent.id == id))
    content = result.scalars().first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    quiz_result = await db.execute(select(Quiz).where(Quiz.content_id == id))
    quiz = quiz_result.scalars().first()
    if not quiz:
        return None
    question_result = await db.execute(select(QuizQuestion).where(QuizQuestion.quiz_id == quiz.id))
    questions = question_result.scalars().all()
    return {
        "id": quiz.id,
        "title": quiz.title,
        "content_id": quiz.content_id,
        "created_at": quiz.created_at,
        "questions": [
            {
                "id": q.id,
                "quiz_id": q.quiz_id,
                "question": q.question,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "correct_option": q.correct_option,
            }
            for q in questions
        ],
    }


@router.post("/{id}/quiz", response_model=QuizOut)
async def create_quiz_for_content(
    id: int,
    payload: QuizCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    result = await db.execute(select(LearningContent).where(LearningContent.id == id))
    content = result.scalars().first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    existing_quiz = await db.execute(select(Quiz).where(Quiz.content_id == id))
    if existing_quiz.scalars().first():
        raise HTTPException(status_code=400, detail="Quiz already exists for this content")
    quiz = Quiz(title=payload.title, content_id=id)
    db.add(quiz)
    await db.flush()
    for question in payload.questions:
        db.add(QuizQuestion(
            quiz_id=quiz.id,
            question=question.question,
            option_a=question.option_a,
            option_b=question.option_b,
            option_c=question.option_c,
            option_d=question.option_d,
            correct_option=question.correct_option,
        ))
    await db.commit()
    await db.refresh(quiz)
    question_result = await db.execute(select(QuizQuestion).where(QuizQuestion.quiz_id == quiz.id))
    questions = question_result.scalars().all()
    return {
        "id": quiz.id,
        "title": quiz.title,
        "content_id": quiz.content_id,
        "created_at": quiz.created_at,
        "questions": [
            {
                "id": q.id,
                "quiz_id": q.quiz_id,
                "question": q.question,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "correct_option": q.correct_option,
            }
            for q in questions
        ],
    }


@router.post("/{id}/quiz/attempt", response_model=QuizAttemptOut)
async def submit_quiz_attempt(
    id: int,
    payload: QuizAttemptSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Student access required")
    student_result = await db.execute(select(Student).where(Student.user_id == current_user.id))
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    quiz_result = await db.execute(select(Quiz).where(Quiz.content_id == id))
    quiz = quiz_result.scalars().first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    questions_result = await db.execute(select(QuizQuestion).where(QuizQuestion.quiz_id == quiz.id))
    questions = questions_result.scalars().all()
    question_map = {q.id: q for q in questions}
    total = len(questions) or 1
    score = 0
    for answer in payload.answers:
        question = question_map.get(answer.question_id)
        if question and str(answer.answer).lower() == question.correct_option.value:
            score += 1
    percentage = round((score / total) * 100, 2)
    attempt = QuizAttempt(quiz_id=quiz.id, student_id=student.id, score=percentage)
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)
    return attempt
