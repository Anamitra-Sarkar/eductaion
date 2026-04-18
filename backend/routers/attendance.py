from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, func
from typing import List, Optional
from datetime import datetime, timedelta
from database import get_db
from models import AttendanceSession, AttendanceRecord, Subject, Student, User, UserRole, AttendanceStatus
from schemas import AttendanceSession as AttendanceSessionSchema, AttendanceSessionCreate, AttendanceRecord as AttendanceRecordSchema, AttendanceRecordCreate, AttendanceSessionWithRecords
from routers.auth import get_current_user

router = APIRouter(prefix="/attendance", tags=["attendance"])

async def verify_faculty_or_admin(token: str, db: AsyncSession) -> User:
    user = await get_current_user(token, db)
    if user.role not in [UserRole.faculty, UserRole.admin]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    return user

@router.get("/sessions", response_model=List[AttendanceSessionWithRecords])
async def get_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    date: Optional[str] = Query(None),
    subject_id: Optional[int] = Query(None),
    dept_id: Optional[int] = Query(None)
):
    query = select(AttendanceSession)
    
    if subject_id:
        query = query.where(AttendanceSession.subject_id == subject_id)
    if date:
        target_date = datetime.fromisoformat(date)
        query = query.where(
            and_(
                AttendanceSession.date >= target_date,
                AttendanceSession.date < target_date + timedelta(days=1)
            )
        )
    
    result = await db.execute(query)
    sessions = result.scalars().all()
    return sessions

@router.post("/sessions", response_model=AttendanceSessionSchema)
async def create_session(session: AttendanceSessionCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in [UserRole.faculty, UserRole.admin]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    
    result = await db.execute(select(Subject).where(Subject.id == session.subject_id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Subject not found")
    
    db_session = AttendanceSession(
        subject_id=session.subject_id,
        date=session.date,
        faculty_id=current_user.id,
        total_students=session.total_students
    )
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    return db_session

@router.post("/sessions/{id}/records")
async def mark_attendance(id: int, records: List[AttendanceRecordCreate], current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in [UserRole.faculty, UserRole.admin]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    
    result = await db.execute(select(AttendanceSession).where(AttendanceSession.id == id))
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    for record in records:
        result = await db.execute(select(AttendanceRecord).where(
            and_(
                AttendanceRecord.session_id == id,
                AttendanceRecord.student_id == record.student_id
            )
        ))
        existing = result.scalars().first()
        
        if existing:
            existing.status = record.status
        else:
            db_record = AttendanceRecord(
                session_id=id,
                student_id=record.student_id,
                status=record.status
            )
            db.add(db_record)
    
    await db.commit()
    return {"message": "Attendance marked"}

@router.put("/records/{id}")
async def update_attendance_record(id: int, record: AttendanceRecordCreate, token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await verify_faculty_or_admin(token, db)
    
    result = await db.execute(select(AttendanceRecord).where(AttendanceRecord.id == id))
    db_record = result.scalars().first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    db_record.status = record.status
    await db.commit()
    await db.refresh(db_record)
    return db_record

@router.get("/report")
async def get_report(
    token: str = Depends(lambda: None),
    db: AsyncSession = Depends(get_db),
    dept_id: Optional[int] = Query(None),
    from_date: Optional[str] = Query(None),
    to_date: Optional[str] = Query(None),
    semester: Optional[int] = Query(None)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await get_current_user(token, db)
    
    query = select(AttendanceRecord)
    
    if from_date and to_date:
        start = datetime.fromisoformat(from_date)
        end = datetime.fromisoformat(to_date)
        query = query.join(AttendanceSession).where(
            and_(
                AttendanceSession.date >= start,
                AttendanceSession.date <= end
            )
        )
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    report = []
    for record in records:
        await db.refresh(record, ["student", "session"])
        report.append({
            "student_id": record.student_id,
            "student_name": record.student.name,
            "date": record.session.date,
            "status": record.status.value,
            "subject": record.session.subject.name
        })
    
    return report

@router.get("/defaulters")
async def get_defaulters(
    token: str = Depends(lambda: None),
    db: AsyncSession = Depends(get_db),
    threshold: float = Query(75),
    dept_id: Optional[int] = Query(None)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await get_current_user(token, db)
    
    query = select(Student)
    if dept_id:
        query = query.where(Student.dept_id == dept_id)
    
    result = await db.execute(query)
    students = result.scalars().all()
    
    defaulters = []
    for student in students:
        result = await db.execute(select(AttendanceRecord).where(AttendanceRecord.student_id == student.id))
        records = result.scalars().all()
        
        total = len(records)
        if total == 0:
            continue
        
        attended = sum(1 for r in records if r.status == AttendanceStatus.present)
        percentage = (attended / total) * 100
        
        if percentage < threshold:
            defaulters.append({
                "student_id": student.id,
                "name": student.name,
                "roll_no": student.roll_no,
                "attendance_percentage": percentage
            })
    
    return defaulters

@router.get("/heatmap")
async def get_heatmap(
    token: str = Depends(lambda: None),
    db: AsyncSession = Depends(get_db),
    dept_id: Optional[int] = Query(None),
    days: int = Query(7)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await get_current_user(token, db)
    
    from_date = datetime.utcnow() - timedelta(days=days)
    
    query = select(AttendanceRecord).join(AttendanceSession).where(
        AttendanceSession.date >= from_date
    )
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    heatmap = {}
    for record in records:
        await db.refresh(record, ["student"])
        date_str = record.session.date.strftime("%Y-%m-%d")
        if date_str not in heatmap:
            heatmap[date_str] = {"present": 0, "absent": 0, "late": 0}
        heatmap[date_str][record.status.value] += 1
    
    return heatmap
