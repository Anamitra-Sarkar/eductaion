from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime
import re

from database import get_db
from models import (
    Internship, InternshipApplication, CareerProfile, Student, User,
    UserRole, InternshipApplicationStatus
)
from schemas import InternshipCreate, InternshipOut, ApplicationOut
from routers.auth import get_current_user

router = APIRouter(prefix="/internships", tags=["internships"])


def _tokenize(value: str) -> set[str]:
    return {token.strip().lower() for token in re.split(r"[,\n;/|]+", value or "") if token.strip()}


def _internship_payload(internship: Internship, posted_by_name: Optional[str] = None, match_score: Optional[float] = None):
    payload = {
        "id": internship.id,
        "title": internship.title,
        "company": internship.company,
        "description": internship.description,
        "skills_required": internship.skills_required,
        "stipend": internship.stipend,
        "duration_months": internship.duration_months,
        "location": internship.location,
        "application_deadline": internship.application_deadline,
        "posted_by": internship.posted_by,
        "created_at": internship.created_at,
        "posted_by_name": posted_by_name,
    }
    if match_score is not None:
        payload["match_score"] = round(match_score, 2)
    return payload


@router.get("", response_model=List[InternshipOut])
async def list_internships(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Internship).order_by(Internship.created_at.desc()))
    internships = result.scalars().all()
    poster_ids = {item.posted_by for item in internships}
    posters = {}
    if poster_ids:
        user_result = await db.execute(select(User).where(User.id.in_(poster_ids)))
        posters = {u.id: u.name for u in user_result.scalars().all()}
    return [_internship_payload(item, posters.get(item.posted_by)) for item in internships]


@router.post("", response_model=InternshipOut)
async def create_internship(
    payload: InternshipCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    internship = Internship(
        title=payload.title,
        company=payload.company,
        description=payload.description,
        skills_required=payload.skills_required,
        stipend=payload.stipend,
        duration_months=payload.duration_months,
        location=payload.location,
        application_deadline=payload.application_deadline,
        posted_by=current_user.id,
    )
    db.add(internship)
    await db.commit()
    await db.refresh(internship)
    return _internship_payload(internship, current_user.name)


@router.get("/recommend")
async def recommend_internships(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Student access required")
    student_result = await db.execute(select(Student).where(Student.user_id == current_user.id))
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    profile_result = await db.execute(select(CareerProfile).where(CareerProfile.student_id == student.id))
    profile = profile_result.scalars().first()
    if not profile:
        return []
    profile_tokens = _tokenize(profile.skills) | _tokenize(profile.interests)
    internships_result = await db.execute(select(Internship))
    internships = internships_result.scalars().all()
    poster_ids = {item.posted_by for item in internships}
    posters = {}
    if poster_ids:
        user_result = await db.execute(select(User).where(User.id.in_(poster_ids)))
        posters = {u.id: u.name for u in user_result.scalars().all()}
    scored = []
    for internship in internships:
        tokens = _tokenize(internship.skills_required) | _tokenize(internship.title) | _tokenize(internship.company)
        if not tokens:
            score = 0.0
        else:
            overlap = len(profile_tokens & tokens)
            score = (overlap / max(len(tokens), 1)) * 100
        scored.append((_internship_payload(internship, posters.get(internship.posted_by)), score))
    scored.sort(key=lambda item: item[1], reverse=True)
    return [{"match_score": round(score, 2), **item} for item, score in scored[:5]]


@router.get("/my-applications", response_model=List[ApplicationOut])
async def my_applications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Student access required")
    student_result = await db.execute(select(Student).where(Student.user_id == current_user.id))
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    result = await db.execute(select(InternshipApplication).where(InternshipApplication.student_id == student.id))
    applications = result.scalars().all()
    internships_result = await db.execute(select(Internship))
    internships = {item.id: item for item in internships_result.scalars().all()}
    return [
        {
            "id": app.id,
            "internship_id": app.internship_id,
            "student_id": app.student_id,
            "status": app.status,
            "applied_at": app.applied_at,
            "internship_title": internships.get(app.internship_id).title if internships.get(app.internship_id) else None,
            "company": internships.get(app.internship_id).company if internships.get(app.internship_id) else None,
            "student_name": current_user.name,
        }
        for app in applications
    ]


@router.get("/applications", response_model=List[ApplicationOut])
async def all_applications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    result = await db.execute(select(InternshipApplication))
    applications = result.scalars().all()
    internship_ids = {app.internship_id for app in applications}
    student_ids = {app.student_id for app in applications}
    internships = {}
    students = {}
    if internship_ids:
        internship_result = await db.execute(select(Internship).where(Internship.id.in_(internship_ids)))
        internships = {item.id: item for item in internship_result.scalars().all()}
    if student_ids:
        student_result = await db.execute(select(Student).where(Student.id.in_(student_ids)))
        students = {item.id: item.name for item in student_result.scalars().all()}
    return [
        {
            "id": app.id,
            "internship_id": app.internship_id,
            "student_id": app.student_id,
            "status": app.status,
            "applied_at": app.applied_at,
            "internship_title": internships.get(app.internship_id).title if internships.get(app.internship_id) else None,
            "company": internships.get(app.internship_id).company if internships.get(app.internship_id) else None,
            "student_name": students.get(app.student_id),
        }
        for app in applications
    ]


@router.get("/{id}")
async def get_internship(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Internship).where(Internship.id == id))
    internship = result.scalars().first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
    poster_result = await db.execute(select(User).where(User.id == internship.posted_by))
    poster = poster_result.scalars().first()
    return _internship_payload(internship, poster.name if poster else None)


@router.post("/{id}/apply")
async def apply_to_internship(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Student access required")
    student_result = await db.execute(select(Student).where(Student.user_id == current_user.id))
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    internship_result = await db.execute(select(Internship).where(Internship.id == id))
    internship = internship_result.scalars().first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
    existing = await db.execute(
        select(InternshipApplication).where(
            InternshipApplication.internship_id == id,
            InternshipApplication.student_id == student.id,
        )
    )
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Already applied")
    application = InternshipApplication(
        internship_id=id,
        student_id=student.id,
        status=InternshipApplicationStatus.applied,
    )
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return {
        "id": application.id,
        "internship_id": application.internship_id,
        "student_id": application.student_id,
        "status": application.status,
        "applied_at": application.applied_at,
    }


@router.put("/applications/{id}/status")
async def update_application_status(
    id: int,
    status: InternshipApplicationStatus = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    result = await db.execute(select(InternshipApplication).where(InternshipApplication.id == id))
    application = result.scalars().first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    application.status = status
    await db.commit()
    await db.refresh(application)
    return {
        "id": application.id,
        "internship_id": application.internship_id,
        "student_id": application.student_id,
        "status": application.status,
        "applied_at": application.applied_at,
    }
