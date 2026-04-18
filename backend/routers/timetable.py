from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from database import get_db
from models import TimetableSlot, Subject, User, UserRole
from schemas import TimetableSlot as TimetableSlotSchema, TimetableSlotCreate, TimetableSlotWithSubject
from routers.auth import get_current_user
from datetime import time

router = APIRouter(prefix="/timetable", tags=["timetable"])

async def verify_admin(token: str, db: AsyncSession) -> User:
    user = await get_current_user(token, db)
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.get("", response_model=List[TimetableSlotWithSubject])
async def get_timetable(
    token: str = Depends(lambda: None),
    db: AsyncSession = Depends(get_db),
    dept_id: Optional[int] = Query(None),
    semester: Optional[int] = Query(None),
    day: Optional[str] = Query(None)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await get_current_user(token, db)
    
    query = select(TimetableSlot)
    
    if dept_id:
        query = query.where(TimetableSlot.dept_id == dept_id)
    if semester:
        query = query.where(TimetableSlot.semester == semester)
    if day:
        query = query.where(TimetableSlot.day == day)
    
    result = await db.execute(query)
    slots = result.scalars().all()
    return slots

@router.post("", response_model=TimetableSlotSchema)
async def create_timetable(slot: TimetableSlotCreate, token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await verify_admin(token, db)
    
    result = await db.execute(select(Subject).where(Subject.id == slot.subject_id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Subject not found")
    
    db_slot = TimetableSlot(
        day=slot.day,
        time_start=slot.time_start,
        time_end=slot.time_end,
        subject_id=slot.subject_id,
        room=slot.room,
        semester=slot.semester,
        dept_id=slot.dept_id
    )
    db.add(db_slot)
    await db.commit()
    await db.refresh(db_slot)
    return db_slot

@router.put("/{id}", response_model=TimetableSlotSchema)
async def update_timetable(id: int, slot: TimetableSlotCreate, token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await verify_admin(token, db)
    
    result = await db.execute(select(TimetableSlot).where(TimetableSlot.id == id))
    db_slot = result.scalars().first()
    if not db_slot:
        raise HTTPException(status_code=404, detail="Timetable slot not found")
    
    db_slot.day = slot.day
    db_slot.time_start = slot.time_start
    db_slot.time_end = slot.time_end
    db_slot.subject_id = slot.subject_id
    db_slot.room = slot.room
    db_slot.semester = slot.semester
    db_slot.dept_id = slot.dept_id
    
    await db.commit()
    await db.refresh(db_slot)
    return db_slot

@router.delete("/{id}")
async def delete_timetable(id: int, token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await verify_admin(token, db)
    
    result = await db.execute(select(TimetableSlot).where(TimetableSlot.id == id))
    db_slot = result.scalars().first()
    if not db_slot:
        raise HTTPException(status_code=404, detail="Timetable slot not found")
    
    await db.delete(db_slot)
    await db.commit()
    return {"message": "Timetable slot deleted"}

@router.get("/conflicts")
async def check_conflicts(
    token: str = Depends(lambda: None),
    db: AsyncSession = Depends(get_db),
    faculty_id: Optional[int] = Query(None),
    day: Optional[str] = Query(None),
    time_start: Optional[str] = Query(None),
    time_end: Optional[str] = Query(None)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await get_current_user(token, db)
    
    query = select(TimetableSlot).join(Subject)
    
    if faculty_id:
        query = query.where(Subject.faculty_id == faculty_id)
    
    result = await db.execute(query)
    slots = result.scalars().all()
    
    conflicts = []
    if day and time_start and time_end:
        time_start_obj = time.fromisoformat(time_start)
        time_end_obj = time.fromisoformat(time_end)
        
        for slot in slots:
            if slot.day == day:
                if not (slot.time_end <= time_start_obj or slot.time_start >= time_end_obj):
                    conflicts.append({
                        "slot_id": slot.id,
                        "subject": slot.subject.name,
                        "day": slot.day,
                        "time_start": str(slot.time_start),
                        "time_end": str(slot.time_end),
                        "room": slot.room
                    })
    
    return conflicts
