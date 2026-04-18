from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from database import get_db
from models import Alumni, Department, User, UserRole
from schemas import Alumni as AlumniSchema, AlumniCreate, AlumniUpdate
from routers.auth import get_current_user

router = APIRouter(prefix="/alumni", tags=["alumni"])

async def verify_admin(token: str, db: AsyncSession) -> User:
    user = await get_current_user(token, db)
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.get("", response_model=List[AlumniSchema])
async def get_alumni(
    token: str = Depends(lambda: None),
    db: AsyncSession = Depends(get_db),
    dept_id: Optional[int] = Query(None),
    batch_year: Optional[int] = Query(None),
    search: Optional[str] = Query(None)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await get_current_user(token, db)
    
    query = select(Alumni)
    
    if dept_id:
        query = query.where(Alumni.dept_id == dept_id)
    if batch_year:
        query = query.where(Alumni.batch_year == batch_year)
    if search:
        query = query.where(
            (Alumni.name.ilike(f"%{search}%")) |
            (Alumni.company.ilike(f"%{search}%")) |
            (Alumni.role.ilike(f"%{search}%"))
        )
    
    result = await db.execute(query)
    alumni = result.scalars().all()
    return alumni

@router.post("", response_model=AlumniSchema)
async def create_alumni(alumni: AlumniCreate, token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await verify_admin(token, db)
    
    result = await db.execute(select(Alumni).where(Alumni.email == alumni.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    result = await db.execute(select(Department).where(Department.id == alumni.dept_id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Department not found")
    
    db_alumni = Alumni(
        name=alumni.name,
        batch_year=alumni.batch_year,
        dept_id=alumni.dept_id,
        company=alumni.company,
        role=alumni.role,
        email=alumni.email,
        linkedin=alumni.linkedin,
        location=alumni.location
    )
    db.add(db_alumni)
    await db.commit()
    await db.refresh(db_alumni)
    return db_alumni

@router.put("/{id}", response_model=AlumniSchema)
async def update_alumni(id: int, alumni_update: AlumniUpdate, token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await verify_admin(token, db)
    
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
async def delete_alumni(id: int, token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await verify_admin(token, db)
    
    result = await db.execute(select(Alumni).where(Alumni.id == id))
    db_alumni = result.scalars().first()
    if not db_alumni:
        raise HTTPException(status_code=404, detail="Alumni not found")
    
    await db.delete(db_alumni)
    await db.commit()
    return {"message": "Alumni record deleted"}
