from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List
from database import get_db
from models import (
    AttendanceRecord, AttendanceStatus, Student, User, UserRole,
    Department, Activity, ActivityEnrollment
)
from schemas import DashboardKPI as DashboardStats
from routers.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(func.count(AttendanceRecord.id)))
    total_attendance_records = result.scalar() or 0
    
    result = await db.execute(select(func.count(Student.id)))
    total_students = result.scalar() or 0
    
    result = await db.execute(select(func.count(Activity.id)))
    total_activities = result.scalar() or 0
    
    result = await db.execute(select(AttendanceRecord).where(AttendanceRecord.status == AttendanceStatus.present))
    present_count = len(result.scalars().all())
    
    attendance_percentage = (present_count / total_attendance_records * 100) if total_attendance_records > 0 else 0
    
    return DashboardStats(
        total_students=total_students,
        total_activities=total_activities,
        total_records=total_attendance_records,
        avg_percentage=attendance_percentage
    )

@router.get("/attendance")
async def get_attendance_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    dept_id: int = None
):
    result = await db.execute(select(Department))
    departments = result.scalars().all()
    
    stats = []
    for dept in departments:
        result = await db.execute(
            select(func.count(AttendanceRecord.id)).where(
                AttendanceRecord.student_id.in_(
                    select(Student.id).where(Student.dept_id == dept.id)
                )
            )
        )
        total = result.scalar() or 0
        
        result = await db.execute(
            select(func.count(AttendanceRecord.id)).where(
                (AttendanceRecord.status == AttendanceStatus.present) &
                (AttendanceRecord.student_id.in_(
                    select(Student.id).where(Student.dept_id == dept.id)
                ))
            )
        )
        present = result.scalar() or 0
        
        percentage = (present / total * 100) if total > 0 else 0
        stats.append({"dept_name": dept.name, "percentage": percentage})
    
    return stats

@router.get("/activities")
async def get_activity_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Activity))
    activities = result.scalars().all()
    
    stats = []
    for activity in activities:
        result = await db.execute(
            select(func.count(ActivityEnrollment.id)).where(ActivityEnrollment.activity_id == activity.id)
        )
        total_enrolled = result.scalar() or 0
        
        result = await db.execute(
            select(func.count(ActivityEnrollment.id)).where(
                (ActivityEnrollment.activity_id == activity.id) &
                (ActivityEnrollment.attended == True)
            )
        )
        attended = result.scalar() or 0
        
        percentage = (attended / total_enrolled * 100) if total_enrolled > 0 else 0
        stats.append({
            "name": activity.name,
            "percentage": percentage,
            "enrolled": total_enrolled,
            "attended": attended
        })
    
    return stats

@router.get("/students/performance")
async def get_student_performance(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student))
    students = result.scalars().all()
    
    performance = []
    for student in students:
        result = await db.execute(
            select(func.count(AttendanceRecord.id)).where(AttendanceRecord.student_id == student.id)
        )
        total_sessions = result.scalar() or 0
        
        result = await db.execute(
            select(func.count(AttendanceRecord.id)).where(
                (AttendanceRecord.student_id == student.id) &
                (AttendanceRecord.status == AttendanceStatus.present)
            )
        )
        attended = result.scalar() or 0
        
        attendance_percentage = (attended / total_sessions * 100) if total_sessions > 0 else 0
        
        result = await db.execute(
            select(func.count(ActivityEnrollment.id)).where(ActivityEnrollment.student_id == student.id)
        )
        total_activities = result.scalar() or 0
        
        result = await db.execute(
            select(func.count(ActivityEnrollment.id)).where(
                (ActivityEnrollment.student_id == student.id) &
                (ActivityEnrollment.attended == True)
            )
        )
        activities_attended = result.scalar() or 0
        
        activity_percentage = (activities_attended / total_activities * 100) if total_activities > 0 else 0
        
        performance.append({
            "student_name": student.name,
            "attendance_percentage": attendance_percentage,
            "activity_percentage": activity_percentage
        })
    
    return performance
