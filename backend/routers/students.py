from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from database import get_db
from models import Student, User, Department, UserRole, StudentStatus
from schemas import Student as StudentSchema, StudentCreate, StudentUpdate, StudentWithDept, StudentAttendanceSummary, StudentActivitySummary
from routers.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/students", tags=["students"])

@router.get("", response_model=List[StudentWithDept])
async def get_students(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    dept_id: Optional[int] = Query(None),
    semester: Optional[int] = Query(None),
    status: Optional[StudentStatus] = Query(None),
    search: Optional[str] = Query(None)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    query = select(Student).options(selectinload(Student.department))
    
    if dept_id:
        query = query.where(Student.dept_id == dept_id)
    if semester:
        query = query.where(Student.semester == semester)
    if status:
        query = query.where(Student.status == status)
    if search:
        query = query.where(
            (Student.name.ilike(f"%{search}%")) |
            (Student.roll_no.ilike(f"%{search}%")) |
            (Student.email.ilike(f"%{search}%"))
        )
    
    result = await db.execute(query)
    students = result.scalars().all()
    return students

@router.get("/{id}", response_model=StudentWithDept)
async def get_student(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Student)
        .options(selectinload(Student.department))
        .where(Student.id == id)
    )
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("", response_model=StudentSchema)
async def create_student(student: StudentCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    
    result = await db.execute(select(Student).where(Student.roll_no == student.roll_no))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Roll number already exists")
    
    result = await db.execute(select(Student).where(Student.email == student.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    result = await db.execute(select(Department).where(Department.id == student.dept_id))
    department = result.scalars().first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    if department.college_id != current_user.college_id:
        raise HTTPException(status_code=403, detail="Department does not belong to your college")
    
    from routers.auth import hash_password
    
    db_user = User(
        name=student.name,
        email=student.email,
        hashed_password=hash_password(student.password),
        role=UserRole.student,
        college_id=current_user.college_id
    )
    db.add(db_user)
    await db.flush()
    
    db_student = Student(
        roll_no=student.roll_no,
        name=student.name,
        dept_id=student.dept_id,
        semester=student.semester,
        phone=student.phone,
        email=student.email,
        status=student.status,
        user_id=db_user.id
    )
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student

@router.put("/{id}", response_model=StudentSchema)
async def update_student(id: int, student_update: StudentUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    
    result = await db.execute(select(Student).where(Student.id == id))
    db_student = result.scalars().first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in student_update.dict(exclude_unset=True).items():
        setattr(db_student, key, value)
    
    await db.commit()
    await db.refresh(db_student)
    return db_student

@router.delete("/{id}")
async def delete_student(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    
    result = await db.execute(select(Student).where(Student.id == id))
    db_student = result.scalars().first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    user_result = await db.execute(select(User).where(User.id == db_student.user_id))
    db_user = user_result.scalars().first()

    if db_user:
        await db.delete(db_user)
    else:
        await db.delete(db_student)

    await db.commit()
    return {"message": "Student deleted"}

@router.get("/{id}/attendance-summary", response_model=StudentAttendanceSummary)
async def get_attendance_summary(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from models import AttendanceRecord, AttendanceStatus
    
    result = await db.execute(select(AttendanceRecord).where(AttendanceRecord.student_id == id))
    records = result.scalars().all()
    
    total_sessions = len(records)
    attended = sum(1 for r in records if r.status == AttendanceStatus.present)
    percentage = (attended / total_sessions * 100) if total_sessions > 0 else 0
    
    return StudentAttendanceSummary(
        total_sessions=total_sessions,
        attended=attended,
        percentage=percentage
    )

@router.get("/{id}/activity-summary", response_model=StudentActivitySummary)
async def get_activity_summary(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from models import ActivityEnrollment
    
    result = await db.execute(select(ActivityEnrollment).where(ActivityEnrollment.student_id == id))
    enrollments = result.scalars().all()
    
    total_enrolled = len(enrollments)
    attended = sum(1 for e in enrollments if e.attended)
    percentage = (attended / total_enrolled * 100) if total_enrolled > 0 else 0
    
    return StudentActivitySummary(
        total_enrolled=total_enrolled,
        attended=attended,
        percentage=percentage
    )
