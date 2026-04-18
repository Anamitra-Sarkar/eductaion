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

class LearningContentType(str, enum.Enum):
    video = "video"
    pdf = "pdf"
    quiz = "quiz"
    text = "text"

class QuizCorrectOption(str, enum.Enum):
    a = "a"
    b = "b"
    c = "c"
    d = "d"

class InternshipApplicationStatus(str, enum.Enum):
    applied = "applied"
    shortlisted = "shortlisted"
    rejected = "rejected"
    selected = "selected"

class DocumentType(str, enum.Enum):
    marksheet = "marksheet"
    certificate = "certificate"
    id_card = "id_card"
    other = "other"

class SessionStatus(str, enum.Enum):
    scheduled = "scheduled"
    live = "live"
    ended = "ended"

class College(Base):
      __tablename__ = "colleges"
      id = Column(Integer, primary_key=True, index=True)
      name = Column(String, unique=True, index=True)
      address = Column(String)
      naac_grade = Column(String)
      principal = Column(String)
      academic_year = Column(String)
      domain = Column(String, nullable=False, default="")
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
    class_sessions = relationship("ClassSession", back_populates="department", cascade="all, delete-orphan")

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
    learning_contents = relationship("LearningContent", back_populates="creator", cascade="all, delete-orphan")
    internships_posted = relationship("Internship", back_populates="poster", cascade="all, delete-orphan")
    documents_verified = relationship("DocumentVerification", back_populates="verifier", foreign_keys="DocumentVerification.verified_by")
    class_sessions = relationship("ClassSession", back_populates="faculty", cascade="all, delete-orphan")

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
    quiz_attempts = relationship("QuizAttempt", back_populates="student", cascade="all, delete-orphan")
    internship_applications = relationship("InternshipApplication", back_populates="student", cascade="all, delete-orphan")
    document_verifications = relationship("DocumentVerification", back_populates="student", cascade="all, delete-orphan")
    career_profile = relationship("CareerProfile", back_populates="student", uselist=False, cascade="all, delete-orphan")

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

class LearningContent(Base):
    __tablename__ = "learning_contents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    subject = Column(String, nullable=False, index=True)
    grade_level = Column(Integer, nullable=False)
    content_type = Column(Enum(LearningContentType), nullable=False)
    url = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    creator = relationship("User", back_populates="learning_contents")
    department = relationship("Department")
    quiz = relationship("Quiz", back_populates="content", uselist=False, cascade="all, delete-orphan")

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content_id = Column(Integer, ForeignKey("learning_contents.id"), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    content = relationship("LearningContent", back_populates="quiz")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    question = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_option = Column(Enum(QuizCorrectOption), nullable=False)
    quiz = relationship("Quiz", back_populates="questions")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    score = Column(Float, nullable=False, default=0)
    attempted_at = Column(DateTime, default=datetime.utcnow)
    quiz = relationship("Quiz", back_populates="attempts")
    student = relationship("Student", back_populates="quiz_attempts")

class Internship(Base):
    __tablename__ = "internships"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    skills_required = Column(Text, nullable=False)
    stipend = Column(Integer, nullable=False)
    duration_months = Column(Integer, nullable=False)
    location = Column(String, nullable=False, index=True)
    application_deadline = Column(DateTime, nullable=False)
    posted_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    poster = relationship("User", back_populates="internships_posted")
    applications = relationship("InternshipApplication", back_populates="internship", cascade="all, delete-orphan")

class InternshipApplication(Base):
    __tablename__ = "internship_applications"
    id = Column(Integer, primary_key=True, index=True)
    internship_id = Column(Integer, ForeignKey("internships.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    status = Column(Enum(InternshipApplicationStatus), default=InternshipApplicationStatus.applied, nullable=False)
    applied_at = Column(DateTime, default=datetime.utcnow)
    internship = relationship("Internship", back_populates="applications")
    student = relationship("Student", back_populates="internship_applications")

class DocumentVerification(Base):
    __tablename__ = "document_verifications"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    filename = Column(String, nullable=False)
    hash = Column(String, index=True, nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    verified_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)
    student = relationship("Student", back_populates="document_verifications")
    verifier = relationship("User", back_populates="documents_verified", foreign_keys=[verified_by])

class CareerProfile(Base):
    __tablename__ = "career_profiles"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, unique=True)
    interests = Column(Text, default="")
    skills = Column(Text, default="")
    target_role = Column(String, default="")
    target_companies = Column(Text, default="")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    student = relationship("Student", back_populates="career_profile")

class ClassSession(Base):
    __tablename__ = "class_sessions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    subject = Column(String, nullable=False, index=True)
    faculty_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    semester = Column(Integer, nullable=False)
    meet_link = Column(String, nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    status = Column(Enum(SessionStatus), default=SessionStatus.scheduled, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    faculty = relationship("User", back_populates="class_sessions")
    department = relationship("Department", back_populates="class_sessions")
