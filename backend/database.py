import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./attendx.db")

if "sqlite" in DATABASE_URL:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        future=True,
        poolclass=NullPool,
    )
else:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        future=True,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    from models import (  # noqa: F401 – registers all models with Base.metadata
        College, Department, User, Student, Subject,
        TimetableSlot, AttendanceSession, AttendanceRecord,
        Activity, ActivityEnrollment, Alumni,
        LearningContent, Course, CourseModule,
        StudentCourseProgress, StudentModuleProgress, StudentXP,
        Quiz, QuizQuestion, QuizAttempt,
        Internship, InternshipApplication,
        DocumentVerification,
        CareerProfile,
        ClassSession,
    )
    async with engine.begin() as conn:
        # Drop all tables and recreate when RESET_DB=true (use once to fix schema drift)
        if os.getenv("RESET_DB", "false").lower() == "true":
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
