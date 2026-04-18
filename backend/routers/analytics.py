from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
from database import get_db
from models import AttendanceRecord, AttendanceSession, Activity, ActivityEnrollment, Student, Department, AttendanceStatus, ActivityStatus
from schemas import DashboardKPI, AttendanceTrendResponse, AttendanceTrend, DepartmentComparison, ActivityCompletionStats
from routers.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard-kpis", response_model=DashboardKPI)
async def get_dashboard_kpis(
    token: str = Depends(lambda: None),
    db: AsyncSession = Depends(get_db),
    dept_id: Optional[int] = Query(None)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await get_current_user(token, db)
    
    today = datetime.utcnow().date()
    
    # Today's attendance percentage
    query = select(AttendanceRecord).join(AttendanceSession).where(
        AttendanceSession.date >= datetime(today.year, today.month, today.day)
    )
    result = await db.execute(query)
    today_records = result.scalars().all()
    
    attendance_percentage = 0
    if today_records:
        present = sum(1 for r in today_records if r.status == AttendanceStatus.present)
        attendance_percentage = (present / len(today_records)) * 100
    
    # Active students
    query = select(func.count(Student.id)).where(Student.status == "active")
    if dept_id:
        query = query.where(Student.dept_id == dept_id)
    result = await db.execute(query)
    active_students = result.scalar() or 0
    
    # Pending activities
    query = select(func.count(Activity.id)).where(Activity.status == "upcoming")
    if dept_id:
        query = query.where(Activity.dept_id == dept_id)
    result = await db.execute(query)
    pending_activities = result.scalar() or 0
    
    # Conflicts (timetable slots in same room at same time)
    conflicts = 0
    
    return DashboardKPI(
        attendance_percentage=round(attendance_percentage, 2),
        active_students=active_students,
        pending_activities=pending_activities,
        conflicts=conflicts
    )

@router.get("/attendance-trend", response_model=AttendanceTrendResponse)
async def get_attendance_trend(
    token: str = Depends(lambda: None),
    db: AsyncSession = Depends(get_db),
    dept_id: Optional[int] = Query(None),
    months: int = Query(6)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await get_current_user(token, db)
    
    from_date = datetime.utcnow() - timedelta(days=30*months)
    
    query = select(AttendanceRecord).join(AttendanceSession).where(
        AttendanceSession.date >= from_date
    )
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    daily_data = {}
    for record in records:
        date_str = record.session.date.strftime("%Y-%m-%d")
        if date_str not in daily_data:
            daily_data[date_str] = {"present": 0, "total": 0}
        daily_data[date_str]["total"] += 1
        if record.status == AttendanceStatus.present:
            daily_data[date_str]["present"] += 1
    
    trends = []
    for date_str in sorted(daily_data.keys()):
        data = daily_data[date_str]
        percentage = (data["present"] / data["total"] * 100) if data["total"] > 0 else 0
        trends.append(AttendanceTrend(date=date_str, percentage=round(percentage, 2)))
    
    return AttendanceTrendResponse(trends=trends)

@router.get("/department-comparison", response_model=List[DepartmentComparison])
async def get_department_comparison(
    token: str = Depends(lambda: None),
    db: AsyncSession = Depends(get_db),
    semester: Optional[int] = Query(None)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await get_current_user(token, db)
    
    query = select(Department)
    result = await db.execute(query)
    departments = result.scalars().all()
    
    comparisons = []
    for dept in departments:
        # Count active students
        student_query = select(func.count(Student.id)).where(
            Student.dept_id == dept.id,
            Student.status == "active"
        )
        result = await db.execute(student_query)
        active_students = result.scalar() or 0
        
        # Calculate attendance percentage
        attendance_query = select(AttendanceRecord).join(AttendanceSession).join(Student).where(
            Student.dept_id == dept.id
        )
        result = await db.execute(attendance_query)
        records = result.scalars().all()
        
        percentage = 0
        if records:
            present = sum(1 for r in records if r.status == AttendanceStatus.present)
            percentage = (present / len(records)) * 100
        
        comparisons.append(DepartmentComparison(
            department=dept.name,
            attendance_percentage=round(percentage, 2),
            active_students=active_students
        ))
    
    return comparisons

@router.get("/activity-completion", response_model=ActivityCompletionStats)
async def get_activity_completion(
    token: str = Depends(lambda: None),
    db: AsyncSession = Depends(get_db),
    year: Optional[int] = Query(None),
    dept_id: Optional[int] = Query(None)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await get_current_user(token, db)
    
    query = select(Activity)
    if dept_id:
        query = query.where(Activity.dept_id == dept_id)
    
    result = await db.execute(query)
    activities = result.scalars().all()
    
    total = len(activities)
    completed = sum(1 for a in activities if a.status == ActivityStatus.completed)
    percentage = (completed / total * 100) if total > 0 else 0
    
    return ActivityCompletionStats(
        total=total,
        completed=completed,
        percentage=round(percentage, 2)
    )
