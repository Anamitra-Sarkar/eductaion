from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from database import get_db
from models import ClassSession, Department, User, UserRole, SessionStatus
from schemas import ClassSessionCreate, ClassSessionOut
from routers.auth import get_current_user

router = APIRouter(prefix="/classroom", tags=["classroom"])


def _payload(session: ClassSession, faculty_name: Optional[str] = None, department_name: Optional[str] = None):
    return {
        "id": session.id,
        "title": session.title,
        "subject": session.subject,
        "faculty_id": session.faculty_id,
        "dept_id": session.dept_id,
        "semester": session.semester,
        "meet_link": session.meet_link,
        "scheduled_at": session.scheduled_at,
        "duration_minutes": session.duration_minutes,
        "status": session.status,
        "created_at": session.created_at,
        "faculty_name": faculty_name,
        "department_name": department_name,
    }


@router.get("/sessions")
async def list_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    dept_id: Optional[int] = Query(None),
    dept: Optional[int] = Query(None, alias="dept"),
    semester: Optional[int] = Query(None),
    status: Optional[SessionStatus] = Query(None),
):
    query = select(ClassSession)
    target_dept = dept_id or dept
    if target_dept:
        query = query.where(ClassSession.dept_id == target_dept)
    if semester:
        query = query.where(ClassSession.semester == semester)
    if status:
        query = query.where(ClassSession.status == status)
    result = await db.execute(query.order_by(ClassSession.scheduled_at.desc()))
    sessions = result.scalars().all()
    faculty_ids = {session.faculty_id for session in sessions}
    dept_ids = {session.dept_id for session in sessions}
    faculty_map = {}
    dept_map = {}
    if faculty_ids:
        faculty_result = await db.execute(select(User).where(User.id.in_(faculty_ids)))
        faculty_map = {user.id: user.name for user in faculty_result.scalars().all()}
    if dept_ids:
        dept_result = await db.execute(select(Department).where(Department.id.in_(dept_ids)))
        dept_map = {dept.id: dept.name for dept in dept_result.scalars().all()}
    return [_payload(session, faculty_map.get(session.faculty_id), dept_map.get(session.dept_id)) for session in sessions]


@router.post("/sessions", response_model=ClassSessionOut)
async def create_session(
    payload: ClassSessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    dept_result = await db.execute(select(Department).where(Department.id == payload.dept_id))
    if not dept_result.scalars().first():
        raise HTTPException(status_code=404, detail="Department not found")
    session = ClassSession(
        title=payload.title,
        subject=payload.subject,
        faculty_id=current_user.id,
        dept_id=payload.dept_id,
        semester=payload.semester,
        meet_link=payload.meet_link,
        scheduled_at=payload.scheduled_at,
        duration_minutes=payload.duration_minutes,
        status=payload.status,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    dept_result = await db.execute(select(Department).where(Department.id == session.dept_id))
    dept = dept_result.scalars().first()
    return _payload(session, current_user.name, dept.name if dept else None)


@router.put("/sessions/{id}/status")
async def update_session_status(
    id: int,
    status: SessionStatus,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    result = await db.execute(select(ClassSession).where(ClassSession.id == id))
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if current_user.role == UserRole.faculty and session.faculty_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own sessions")
    session.status = status
    await db.commit()
    await db.refresh(session)
    return {"id": session.id, "status": session.status}


@router.delete("/sessions/{id}")
async def delete_session(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    result = await db.execute(select(ClassSession).where(ClassSession.id == id))
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if current_user.role == UserRole.faculty and session.faculty_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own sessions")
    await db.delete(session)
    await db.commit()
    return {"message": "Session deleted"}
