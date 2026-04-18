from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List
from database import get_db
from models import College

router = APIRouter(prefix="/colleges", tags=["colleges"])

class CollegePublic(BaseModel):
    id: int
    name: str
    domain: str

@router.get("", response_model=List[CollegePublic])
async def get_colleges(db: AsyncSession = Depends(get_db)):
    """Get all colleges with id, name, and domain. Public endpoint."""
    result = await db.execute(select(College))
    colleges = result.scalars().all()
    return [CollegePublic(id=c.id, name=c.name, domain=c.domain) for c in colleges]
