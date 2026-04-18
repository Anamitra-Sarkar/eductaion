from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager
from database import init_db
from routers import auth, colleges, students, attendance, timetable, activities, alumni, analytics, learning, internships, documents, career, classroom, departments

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    if os.getenv("RUN_SEED", "false").lower() == "true":
        from seed import seed_all
        await seed_all()
    yield

app = FastAPI(
    title="AttendX API",
    description="Smart Curriculum Activity & Attendance Monitoring System",
    version="1.0.0",
    lifespan=lifespan
)

DEFAULT_ORIGINS = [
    "https://eductaion-phi.vercel.app",
    "https://eductaion.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

frontend_url = os.getenv("FRONTEND_URL", "")
if frontend_url:
    extra = [o.strip().rstrip("/") for o in frontend_url.split(",") if o.strip()]
    origins = list(set(DEFAULT_ORIGINS + extra))
else:
    origins = DEFAULT_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(auth.router)
app.include_router(colleges.router)
app.include_router(students.router)
app.include_router(attendance.router)
app.include_router(timetable.router)
app.include_router(activities.router)
app.include_router(alumni.router)
app.include_router(analytics.router)
app.include_router(learning.router)
app.include_router(internships.router)
app.include_router(documents.router)
app.include_router(career.router)
app.include_router(classroom.router)
app.include_router(departments.router)

@app.get("/")
async def root():
    return {"message": "AttendX API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
