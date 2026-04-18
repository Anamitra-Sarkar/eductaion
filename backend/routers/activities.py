from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from database import get_db
from models import Activity, ActivityEnrollment, Student, User, UserRole, ActivityStatus, ActivityType
from schemas import Activity as ActivitySchema, ActivityCreate, ActivityUpdate
from routers.auth import get_current_user

router = APIRouter(prefix="/activities", tags=["activities"])

@router.get("", response_model=List[ActivitySchema])
async def get_activities(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    activity_type: Optional[ActivityType] = Query(None),
    status: Optional[ActivityStatus] = Query(None)
):
    query = select(Activity)
    if activity_type:
        query = query.where(Activity.activity_type == activity_type)
    if status:
        query = query.where(Activity.status == status)
    result = await db.execute(query)
    activities = result.scalars().all()
    return activities

@router.get("/{id}", response_model=ActivitySchema)
async def get_activity(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Activity).where(Activity.id == id))
    activity = result.scalars().first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.post("", response_model=ActivitySchema)
async def create_activity(activity: ActivityCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in [UserRole.faculty, UserRole.admin]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    db_activity = Activity(
        title=activity.title,
        activity_type=activity.activity_type,
        date=activity.date,
        description=activity.description,
        dept_id=activity.dept_id,
        coordinator_id=current_user.id,
        max_capacity=activity.max_capacity,
        status=activity.status
    )
    db.add(db_activity)
    await db.commit()
    await db.refresh(db_activity)
    return db_activity

@router.put("/{id}", response_model=ActivitySchema)
async def update_activity(id: int, activity_update: ActivityUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in [UserRole.faculty, UserRole.admin]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
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
async def delete_activity(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in [UserRole.faculty, UserRole.admin]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    result = await db.execute(select(Activity).where(Activity.id == id))
    db_activity = result.scalars().first()
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    await db.delete(db_activity)
    await db.commit()
    return {"message": "Activity deleted"}

@router.post("/{id}/enroll")
async def enroll_activity(id: int, student_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Activity).where(Activity.id == id))
    activity = result.scalars().first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    result = await db.execute(select(Student).where(Student.id == student_id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Student not found")
    result = await db.execute(select(ActivityEnrollment).where(
        (ActivityEnrollment.activity_id == id) & (ActivityEnrollment.student_id == student_id)
    ))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Student already enrolled")
    enrollment = ActivityEnrollment(activity_id=id, student_id=student_id)
    db.add(enrollment)
    await db.commit()
    return {"message": "Enrolled successfully"}

@router.post("/{id}/mark-attended/{student_id}")
async def mark_attended(id: int, student_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in [UserRole.faculty, UserRole.admin]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    result = await db.execute(select(ActivityEnrollment).where(
        (ActivityEnrollment.activity_id == id) & (ActivityEnrollment.student_id == student_id)
    ))
    enrollment = result.scalars().first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enrollment.attended = True
    await db.commit()
    return {"message": "Marked as attended"}
