import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy import text

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./attendx.db")

# Render provides postgresql:// but asyncpg requires postgresql+asyncpg://
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

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


async def _schema_is_valid(conn) -> bool:
    """
    Quick sanity-check: verify that key columns added in recent migrations
    actually exist in the live DB. Returns False if any are missing.
    """
    # List of (table, column) pairs that must exist for the app to work.
    required_columns = [
        ("colleges", "domain"),
    ]
    try:
        for table, column in required_columns:
            if "sqlite" in DATABASE_URL:
                result = await conn.execute(text(f"PRAGMA table_info({table})"))
                rows = result.fetchall()
                col_names = [row[1] for row in rows]
            else:
                result = await conn.execute(
                    text(
                        "SELECT column_name FROM information_schema.columns "
                        "WHERE table_name = :t AND column_name = :c"
                    ),
                    {"t": table, "c": column},
                )
                col_names = [row[0] for row in result.fetchall()]
            if column not in col_names:
                print(f"[DB] Schema drift detected: column '{column}' missing from '{table}'")
                return False
        return True
    except Exception as e:
        print(f"[DB] Schema check failed: {e}")
        return False


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
        # Explicit reset via env var (one-time use)
        if os.getenv("RESET_DB", "false").lower() == "true":
            print("[DB] RESET_DB=true — dropping and recreating all tables")
            await conn.run_sync(Base.metadata.drop_all)
        else:
            # Auto-reset if schema drift is detected
            valid = await _schema_is_valid(conn)
            if not valid:
                print("[DB] Auto-resetting schema due to drift")
                await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("[DB] Schema is up to date")


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
