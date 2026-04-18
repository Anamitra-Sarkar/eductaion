from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from database import get_db
from models import Alumni, User
from schemas import Alumni as AlumniSchema, AlumniCreate, AlumniUpdate
from routers.auth import get_current_user

router = APIRouter(prefix="/alumni", tags=["alumni"])

@router.get("", response_model=List[AlumniSchema])
async def get_alumni(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    batch: Optional[int] = Query(None),
    dept: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    query = select(Alumni)
    
    if batch:
        query = query.where(Alumni.batch == batch)
    if dept:
        query = query.where(Alumni.dept == dept)
    if search:
        query = query.where(
            (Alumni.name.ilike(f"%{search}%")) |
            (Alumni.company.ilike(f"%{search}%")) |
            (Alumni.email.ilike(f"%{search}%"))
        )
    
    result = await db.execute(query)
    alumni = result.scalars().all()
    return alumni

@router.get("/{id}", response_model=AlumniSchema)
async def get_alumni_by_id(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alumni).where(Alumni.id == id))
    alumni = result.scalars().first()
    if not alumni:
        raise HTTPException(status_code=404, detail="Alumni not found")
    return alumni

@router.post("", response_model=AlumniSchema)
async def create_alumni(alumni: AlumniCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_alumni = Alumni(
        name=alumni.name,
        roll_no=alumni.roll_no,
        batch=alumni.batch,
        dept=alumni.dept,
        email=alumni.email,
        phone=alumni.phone,
        company=alumni.company,
        position=alumni.position,
        linkedin=alumni.linkedin
    )
    db.add(db_alumni)
    await db.commit()
    await db.refresh(db_alumni)
    return db_alumni

@router.put("/{id}", response_model=AlumniSchema)
async def update_alumni(id: int, alumni_update: AlumniUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alumni).where(Alumni.id == id))
    db_alumni = result.scalars().first()
    if not db_alumni:
        raise HTTPException(status_code=404, detail="Alumni not found")
    
    for key, value in alumni_update.dict(exclude_unset=True).items():
        setattr(db_alumni, key, value)
    
    await db.commit()
    await db.refresh(db_alumni)
    return db_alumni

@router.delete("/{id}")
async def delete_alumni(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alumni).where(Alumni.id == id))
    db_alumni = result.scalars().first()
    if not db_alumni:
        raise HTTPException(status_code=404, detail="Alumni not found")
    
    await db.delete(db_alumni)
    await db.commit()
    return {"message": "Alumni deleted"}
