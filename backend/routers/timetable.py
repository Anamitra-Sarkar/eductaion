from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from database import get_db
from models import TimetableSlot, Subject, User, UserRole
from schemas import TimetableSlot as TimetableSlotSchema, TimetableSlotCreate, TimetableSlotWithSubject
from routers.auth import get_current_user
from datetime import time

router = APIRouter(prefix="/timetable", tags=["timetable"])

@router.get("", response_model=List[TimetableSlotWithSubject])
async def get_timetable(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    dept_id: Optional[int] = Query(None),
    semester: Optional[int] = Query(None),
    day: Optional[str] = Query(None)
):
    query = select(TimetableSlot).options(selectinload(TimetableSlot.subject))
    
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
async def create_timetable(slot: TimetableSlotCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    
    result = await db.execute(select(Subject).where(Subject.id == slot.subject_id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Subject not found")
    
    db_slot = TimetableSlot(
        day=slot.day,
        time_start=slot.time_start,
        time_end=slot.time_end,
        subject_id=slot.subject_id,
        room=slot.room,
        dept_id=slot.dept_id,
        semester=slot.semester
    )
    db.add(db_slot)
    await db.commit()
    await db.refresh(db_slot)
    return db_slot

@router.put("/{id}", response_model=TimetableSlotSchema)
async def update_timetable(id: int, slot: TimetableSlotCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    
    result = await db.execute(select(TimetableSlot).where(TimetableSlot.id == id))
    db_slot = result.scalars().first()
    if not db_slot:
        raise HTTPException(status_code=404, detail="Timetable slot not found")
    
    for key, value in slot.dict(exclude_unset=True).items():
        setattr(db_slot, key, value)
    
    await db.commit()
    await db.refresh(db_slot)
    return db_slot

@router.delete("/{id}")
async def delete_timetable(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in [UserRole.admin, UserRole.faculty]:
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    
    result = await db.execute(select(TimetableSlot).where(TimetableSlot.id == id))
    db_slot = result.scalars().first()
    if not db_slot:
        raise HTTPException(status_code=404, detail="Timetable slot not found")
    
    await db.delete(db_slot)
    await db.commit()
    return {"message": "Timetable slot deleted"}
