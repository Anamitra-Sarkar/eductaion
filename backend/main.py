from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager
from database import init_db
from routers import auth, students, attendance, timetable, activities, alumni, analytics

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="AttendX API",
    description="Smart Curriculum Activity & Attendance Monitoring System",
    version="1.0.0",
    lifespan=lifespan
)

frontend_url = os.getenv("FRONTEND_URL", "*")
if frontend_url == "*":
    origins = ["*"]
else:
    origins = [o.strip() for o in frontend_url.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=origins != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(attendance.router)
app.include_router(timetable.router)
app.include_router(activities.router)
app.include_router(alumni.router)
app.include_router(analytics.router)

@app.get("/")
async def root():
    return {"message": "AttendX API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
