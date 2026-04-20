from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List
from database import get_db
from models import (
    AttendanceRecord, AttendanceStatus, Student, User, UserRole,
    Department, Activity, ActivityEnrollment, ActivityStatus, TimetableSlot
)
from routers.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])


def _slots_overlap(left: TimetableSlot, right: TimetableSlot) -> bool:
    if not left.time_start or not left.time_end or not right.time_start or not right.time_end:
        return False
    return left.time_start < right.time_end and right.time_start < left.time_end

@router.get("/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(func.count(AttendanceRecord.id)))
    total_records = result.scalar() or 0

    result = await db.execute(
        select(func.count(Student.id)).where(Student.status == "active")
    )
    active_students = result.scalar() or 0

    result = await db.execute(
        select(func.count(Activity.id)).where(Activity.status == ActivityStatus.upcoming)
    )
    pending_activities = result.scalar() or 0

    result = await db.execute(
        select(func.count(AttendanceRecord.id)).where(AttendanceRecord.status == AttendanceStatus.present)
    )
    present_count = result.scalar() or 0

    attendance_percentage = (present_count / total_records * 100) if total_records > 0 else 0

    slot_result = await db.execute(select(TimetableSlot))
    slots = slot_result.scalars().all()
    conflicts = 0
    for index, left in enumerate(slots):
        for right in slots[index + 1:]:
            if left.day != right.day:
                continue
            if not _slots_overlap(left, right):
                continue
            same_room = bool(left.room and right.room and left.room.strip().lower() == right.room.strip().lower())
            same_group = left.dept_id == right.dept_id and left.semester == right.semester
            if same_room or same_group:
                conflicts += 1

    return {
        "attendance_percentage": round(attendance_percentage, 2),
        "active_students": active_students,
        "pending_activities": pending_activities,
        "conflicts": conflicts
    }

@router.get("/attendance")
async def get_attendance_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
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
        stats.append({"dept_name": dept.name, "percentage": round(percentage, 2)})
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
            "name": activity.title,
            "percentage": round(percentage, 2),
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
        attendance_pct = (attended / total_sessions * 100) if total_sessions > 0 else 0
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
        activity_pct = (activities_attended / total_activities * 100) if total_activities > 0 else 0
        performance.append({
            "student_name": student.name,
            "attendance_percentage": round(attendance_pct, 2),
            "activity_percentage": round(activity_pct, 2)
        })
    return performance
