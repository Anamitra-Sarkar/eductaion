from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_db
from models import Department

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("")
async def get_departments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Department))
    departments = result.scalars().all()
    return [{"id": d.id, "name": d.name, "code": d.code} for d in departments]
