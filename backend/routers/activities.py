from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from typing import List, Optional
from database import get_db
from models import Activity, ActivityEnrollment, Student, User, UserRole, ActivityStatus, ActivityType
from schemas import Activity as ActivitySchema, ActivityCreate, ActivityUpdate, ActivityEnrollment as ActivityEnrollmentSchema
from routers.auth import get_current_user

router = APIRouter(prefix="/activities", tags=["activities"])

async def verify_faculty_or_admin(token: str, db: AsyncSession) -> User:
    user = await get_current_user(token, db)
    if user.role not in [UserRole.faculty, UserRole.admin]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    return user

@router.get("", response_model=List[ActivitySchema])
async def get_activities(
    token: str = Depends(lambda: None),
    db: AsyncSession = Depends(get_db),
    dept_id: Optional[int] = Query(None),
    type: Optional[ActivityType] = Query(None),
    status: Optional[ActivityStatus] = Query(None),
    year: Optional[int] = Query(None)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await get_current_user(token, db)
    
    query = select(Activity)
    
    if dept_id:
        query = query.where(Activity.dept_id == dept_id)
    if type:
        query = query.where(Activity.type == type)
    if status:
        query = query.where(Activity.status == status)
    
    result = await db.execute(query)
    activities = result.scalars().all()
    return activities

@router.post("", response_model=ActivitySchema)
async def create_activity(activity: ActivityCreate, token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user = await verify_faculty_or_admin(token, db)
    
    db_activity = Activity(
        title=activity.title,
        type=activity.type,
        date=activity.date,
        description=activity.description,
        dept_id=activity.dept_id,
        coordinator_id=user.id,
        max_capacity=activity.max_capacity,
        status=activity.status
    )
    db.add(db_activity)
    await db.commit()
    await db.refresh(db_activity)
    return db_activity

@router.put("/{id}", response_model=ActivitySchema)
async def update_activity(id: int, activity_update: ActivityUpdate, token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await verify_faculty_or_admin(token, db)
    
    result = await db.execute(select(Activity).where(Activity.id == id))
    db_activity = result.scalars().first()
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    for key, value in activity_update.dict(exclude_unset=True).items():
        setattr(db_activity, key, value)
    
    await db.commit()
    await db.refresh(db_activity)
    return db_activity

@router.delete("/{id}")
async def delete_activity(id: int, token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await verify_faculty_or_admin(token, db)
    
    result = await db.execute(select(Activity).where(Activity.id == id))
    db_activity = result.scalars().first()
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    await db.delete(db_activity)
    await db.commit()
    return {"message": "Activity deleted"}

@router.post("/{id}/enroll")
async def enroll_students(id: int, student_ids: List[int], token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await verify_faculty_or_admin(token, db)
    
    result = await db.execute(select(Activity).where(Activity.id == id))
    activity = result.scalars().first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    for student_id in student_ids:
        result = await db.execute(select(Student).where(Student.id == student_id))
        if not result.scalars().first():
            continue
        
        result = await db.execute(select(ActivityEnrollment).where(
            and_(
                ActivityEnrollment.activity_id == id,
                ActivityEnrollment.student_id == student_id
            )
        ))
        if not result.scalars().first():
            enrollment = ActivityEnrollment(
                activity_id=id,
                student_id=student_id,
                attended=False
            )
            db.add(enrollment)
    
    await db.commit()
    return {"message": "Students enrolled"}

@router.put("/{id}/mark-attendance")
async def mark_activity_attendance(id: int, enrollments: List[dict], token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await verify_faculty_or_admin(token, db)
    
    result = await db.execute(select(Activity).where(Activity.id == id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Activity not found")
    
    for enrollment_data in enrollments:
        result = await db.execute(select(ActivityEnrollment).where(
            ActivityEnrollment.id == enrollment_data["enrollment_id"]
        ))
        enrollment = result.scalars().first()
        if enrollment:
            enrollment.attended = enrollment_data.get("attended", False)
    
    await db.commit()
    return {"message": "Attendance marked"}
