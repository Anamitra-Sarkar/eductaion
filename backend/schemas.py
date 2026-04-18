from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, time
from typing import Optional, List
from models import UserRole, AttendanceStatus, ActivityType, ActivityStatus, StudentStatus

class CollegeBase(BaseModel):
    name: str
    address: str
    naac_grade: Optional[str] = None
    principal: str
    academic_year: str

class CollegeCreate(CollegeBase):
    pass

class College(CollegeBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class DepartmentBase(BaseModel):
    name: str
    code: str
    college_id: int

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    college_id: int

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class StudentBase(BaseModel):
    roll_no: str
    name: str
    dept_id: int
    semester: int
    phone: str
    email: EmailStr
    status: StudentStatus = StudentStatus.active

class StudentCreate(StudentBase):
    password: str = Field(min_length=6)

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    semester: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[StudentStatus] = None

class Student(StudentBase):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class StudentWithDept(Student):
    department: Department

class SubjectBase(BaseModel):
    code: str
    name: str
    dept_id: int
    semester: int
    faculty_id: Optional[int] = None
    credit_hours: float

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    id: int
    class Config:
        from_attributes = True

class TimetableSlotBase(BaseModel):
    day: str
    time_start: time
    time_end: time
    subject_id: int
    room: str
    semester: int
    dept_id: int

class TimetableSlotCreate(TimetableSlotBase):
    pass

class TimetableSlot(TimetableSlotBase):
    id: int
    class Config:
        from_attributes = True

class TimetableSlotWithSubject(TimetableSlot):
    subject: Subject

class AttendanceRecordBase(BaseModel):
    student_id: int
    status: AttendanceStatus

class AttendanceRecordCreate(AttendanceRecordBase):
    pass

class AttendanceRecord(AttendanceRecordBase):
    id: int
    session_id: int
    updated_at: datetime
    class Config:
        from_attributes = True

class AttendanceSessionBase(BaseModel):
    subject_id: int
    date: datetime
    total_students: int

class AttendanceSessionCreate(AttendanceSessionBase):
    pass

class AttendanceSession(AttendanceSessionBase):
    id: int
    faculty_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class AttendanceSessionWithRecords(AttendanceSession):
    records: List[AttendanceRecord]

class ActivityBase(BaseModel):
    title: str
    activity_type: ActivityType
    date: datetime
    description: str
    dept_id: int
    max_capacity: int
    status: ActivityStatus = ActivityStatus.upcoming

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    activity_type: Optional[ActivityType] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
    max_capacity: Optional[int] = None
    status: Optional[ActivityStatus] = None

class Activity(ActivityBase):
    id: int
    coordinator_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ActivityEnrollmentBase(BaseModel):
    student_id: int
    attended: bool = False

class ActivityEnrollmentCreate(ActivityEnrollmentBase):
    pass

class ActivityEnrollment(ActivityEnrollmentBase):
    id: int
    activity_id: int
    enrolled_at: datetime
    class Config:
        from_attributes = True

class AlumniBase(BaseModel):
    name: str
    batch_year: int
    dept_id: int
    company: str
    role: str
    email: EmailStr
    linkedin: Optional[str] = None
    location: str

class AlumniCreate(AlumniBase):
    pass

class AlumniUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    email: Optional[EmailStr] = None
    linkedin: Optional[str] = None
    location: Optional[str] = None

class Alumni(AlumniBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class DashboardKPI(BaseModel):
    attendance_percentage: float
    active_students: int
    pending_activities: int
    conflicts: int

class AttendanceTrend(BaseModel):
    date: str
    percentage: float

class AttendanceTrendResponse(BaseModel):
    trends: List[AttendanceTrend]

class DepartmentComparison(BaseModel):
    department: str
    attendance_percentage: float
    active_students: int

class ActivityCompletionStats(BaseModel):
    total: int
    completed: int
    percentage: float

class StudentAttendanceSummary(BaseModel):
    total_sessions: int
    attended: int
    percentage: float

class StudentActivitySummary(BaseModel):
    total_enrolled: int
    attended: int
    percentage: float
