from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager
from database import init_db, get_db
from routers import auth, students, attendance, timetable, activities, alumni, analytics

# App startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="AttendX API",
    description="Smart Curriculum Activity & Attendance Monitoring System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
origins = os.getenv("FRONTEND_URL", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
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
