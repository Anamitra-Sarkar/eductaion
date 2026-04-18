from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum, Time, Float, Text
from sqlalchemy.orm import relationship
from database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    faculty = "faculty"
    student = "student"

class AttendanceStatus(str, enum.Enum):
    present = "present"
    absent = "absent"
    late = "late"

class ActivityType(str, enum.Enum):
    workshop = "workshop"
    seminar = "seminar"
    hackathon = "hackathon"
    competition = "competition"
    industrial_visit = "industrial_visit"
    other = "other"

class ActivityStatus(str, enum.Enum):
    upcoming = "upcoming"
    ongoing = "ongoing"
    completed = "completed"
    cancelled = "cancelled"

class StudentStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    graduated = "graduated"

class College(Base):
    __tablename__ = "colleges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    address = Column(String)
    naac_grade = Column(String)
    principal = Column(String)
    academic_year = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    departments = relationship("Department", back_populates="college", cascade="all, delete-orphan")
    users = relationship("User", back_populates="college", cascade="all, delete-orphan")

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False)
    college = relationship("College", back_populates="departments")
    students = relationship("Student", back_populates="department", cascade="all, delete-orphan")
    subjects = relationship("Subject", back_populates="department", cascade="all, delete-orphan")
    timetable_slots = relationship("TimetableSlot", back_populates="department", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="department", cascade="all, delete-orphan")
    alumni = relationship("Alumni", back_populates="department", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.student)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    college = relationship("College", back_populates="users")
    student = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    subjects_as_faculty = relationship("Subject", back_populates="faculty", foreign_keys="Subject.faculty_id")
    attendance_sessions = relationship("AttendanceSession", back_populates="faculty", cascade="all, delete-orphan")
    activities_coordinated = relationship("Activity", back_populates="coordinator", cascade="all, delete-orphan")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    roll_no = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    semester = Column(Integer)
    phone = Column(String)
    email = Column(String, unique=True, index=True)
    status = Column(Enum(StudentStatus), default=StudentStatus.active)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    department = relationship("Department", back_populates="students")
    user = relationship("User", back_populates="student")
    attendance_records = relationship("AttendanceRecord", back_populates="student", cascade="all, delete-orphan")
    activity_enrollments = relationship("ActivityEnrollment", back_populates="student", cascade="all, delete-orphan")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    semester = Column(Integer)
    faculty_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    credit_hours = Column(Float)
    department = relationship("Department", back_populates="subjects")
    faculty = relationship("User", back_populates="subjects_as_faculty", foreign_keys=[faculty_id])
    timetable_slots = relationship("TimetableSlot", back_populates="subject", cascade="all, delete-orphan")
    attendance_sessions = relationship("AttendanceSession", back_populates="subject", cascade="all, delete-orphan")

class TimetableSlot(Base):
    __tablename__ = "timetable_slots"
    id = Column(Integer, primary_key=True, index=True)
    day = Column(String)
    time_start = Column(Time)
    time_end = Column(Time)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    room = Column(String)
    semester = Column(Integer)
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    subject = relationship("Subject", back_populates="timetable_slots")
    department = relationship("Department", back_populates="timetable_slots")

class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    date = Column(DateTime)
    faculty_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_students = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    subject = relationship("Subject", back_populates="attendance_sessions")
    faculty = relationship("User", back_populates="attendance_sessions")
    records = relationship("AttendanceRecord", back_populates="session", cascade="all, delete-orphan")

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("attendance_sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.absent)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    session = relationship("AttendanceSession", back_populates="records")
    student = relationship("Student", back_populates="attendance_records")

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    activity_type = Column(Enum(ActivityType))
    date = Column(DateTime)
    description = Column(Text)
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    coordinator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    max_capacity = Column(Integer)
    status = Column(Enum(ActivityStatus), default=ActivityStatus.upcoming)
    created_at = Column(DateTime, default=datetime.utcnow)
    department = relationship("Department", back_populates="activities")
    coordinator = relationship("User", back_populates="activities_coordinated")
    enrollments = relationship("ActivityEnrollment", back_populates="activity", cascade="all, delete-orphan")

class ActivityEnrollment(Base):
    __tablename__ = "activity_enrollments"
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    attended = Column(Boolean, default=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    activity = relationship("Activity", back_populates="enrollments")
    student = relationship("Student", back_populates="activity_enrollments")

class Alumni(Base):
    __tablename__ = "alumni"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    batch_year = Column(Integer)
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    company = Column(String)
    role = Column(String)
    email = Column(String, unique=True, index=True)
    linkedin = Column(String)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    department = relationship("Department", back_populates="alumni")
