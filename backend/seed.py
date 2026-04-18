import os
import asyncio
from datetime import datetime, timedelta
from database import AsyncSessionLocal, init_db
from models import College, Department, User, Student, Subject, TimetableSlot, AttendanceSession, AttendanceRecord, Activity, ActivityEnrollment, Alumni
from models import (
    UserRole, AttendanceStatus, ActivityType, ActivityStatus, StudentStatus,
    LearningContent, LearningContentType, Quiz, QuizQuestion, QuizCorrectOption,
    Internship, InternshipApplicationStatus, ClassSession, SessionStatus
)
from routers.auth import hash_password
import random

FIRST_NAMES_MALE = ["Rajesh", "Amit", "Vikram", "Arjun", "Harsh", "Nikhil", "Sanjay", "Rohan", "Aditya", "Gaurav"]
FIRST_NAMES_FEMALE = ["Priya", "Neha", "Anjali", "Shreya", "Pooja", "Divya", "Ritika", "Sonali", "Meera", "Isha"]
LAST_NAMES = ["Kumar", "Singh", "Patel", "Sharma", "Gupta", "Reddy", "Verma", "Rao", "Khan", "Nair"]

DEPARTMENTS = [
    ("Computer Science", "CSE"),
    ("Electronics & Communication", "ECE"),
    ("Mechanical Engineering", "MECH"),
    ("Civil Engineering", "CIVIL")
]

SUBJECTS_BY_DEPT = {
    "CSE": [
        ("CS101", "Data Structures", 4),
        ("CS102", "Database Systems", 4),
        ("CS103", "Web Development", 3),
        ("CS104", "Algorithms", 4),
        ("CS105", "Machine Learning", 3),
    ],
    "ECE": [
        ("EC101", "Digital Electronics", 4),
        ("EC102", "Microprocessors", 4),
        ("EC103", "Signals & Systems", 4),
        ("EC104", "Communication Systems", 3),
    ],
    "MECH": [
        ("ME101", "Thermodynamics", 4),
        ("ME102", "Fluid Mechanics", 4),
        ("ME103", "Machine Design", 3),
        ("ME104", "Manufacturing", 4),
    ],
    "CIVIL": [
        ("CE101", "Structural Analysis", 4),
        ("CE102", "Concrete Technology", 4),
        ("CE103", "Geotechnical Engineering", 3),
        ("CE104", "Hydraulics", 4),
    ]
}

ACTIVITY_TYPES = [
    ("Tech Hackathon 2024", "hackathon"),
    ("Coding Workshop", "workshop"),
    ("Tech Seminar", "seminar"),
    ("Programming Competition", "competition"),
    ("Industry Visit", "industrial_visit"),
]

COMPANIES = ["TCS", "Infosys", "Google", "Microsoft", "Amazon", "Adobe", "Flipkart", "Jio", "DRDO", "ISRO"]

async def seed_database():
    await init_db()
    
    async with AsyncSessionLocal() as db:
        # 1. Create College
        college = College(
            name="Institute of Technology Excellence",
            address="123 Campus Road, Bangalore, India",
            naac_grade="A+",
            principal="Dr. A.K. Sharma",
            academic_year="2024-2025",
            domain="student.edu"
        )
        db.add(college)
        await db.flush()
        college_id = college.id
        
        # 2. Create Departments
        dept_map = {}
        for name, code in DEPARTMENTS:
            dept = Department(name=name, code=code, college_id=college_id)
            db.add(dept)
            await db.flush()
            dept_map[code] = dept.id
        
        # 3. Create Admin User
        admin = User(
            name="Administrator",
            email="admin@attendx.edu",
            hashed_password=hash_password("Admin@123"),
            role=UserRole.admin,
            college_id=college_id
        )
        db.add(admin)
        await db.flush()
        admin_id = admin.id

        # 4. Create Faculty Users
        faculty_list = []
        faculty_names = [
            ("Dr. Ramesh Kumar", "faculty@attendx.edu"),
            ("Prof. Sneha Verma", "sneha@attendx.edu"),
            ("Dr. Ajay Sharma", "ajay@attendx.edu"),
            ("Prof. Divya Patel", "divya@attendx.edu"),
        ]

        for name, email in faculty_names:
            faculty = User(
                name=name,
                email=email,
                hashed_password=hash_password("Faculty@123"),
                role=UserRole.faculty,
                college_id=college_id
            )
            db.add(faculty)
            await db.flush()
            faculty_list.append(faculty.id)
        
        # 5. Create Subjects
        subject_map = {}
        faculty_idx = 0
        for dept_code, subjects in SUBJECTS_BY_DEPT.items():
            for code, name, credits in subjects:
                subject = Subject(
                    code=code,
                    name=name,
                    dept_id=dept_map[dept_code],
                    semester=random.randint(1, 8),
                    faculty_id=faculty_list[faculty_idx % len(faculty_list)],
                    credit_hours=credits
                )
                db.add(subject)
                await db.flush()
                subject_map[code] = subject.id
                faculty_idx += 1
        
        # 6. Create Students (30 students across departments)
        student_list = []
        roll_counter = {"CSE": 1, "ECE": 1, "MECH": 1, "CIVIL": 1}
        
        for _ in range(30):
            dept_code = random.choice(list(DEPARTMENTS))[1]
            is_male = random.choice([True, False])
            first_name = random.choice(FIRST_NAMES_MALE if is_male else FIRST_NAMES_FEMALE)
            last_name = random.choice(LAST_NAMES)
            full_name = f"{first_name} {last_name}"
            
            roll_no = f"{dept_code}-{roll_counter[dept_code]:03d}"
            roll_counter[dept_code] += 1
            
            student_user = User(
                name=full_name,
                email=f"{full_name.lower().replace(' ', '.')}@student.edu",
                hashed_password=hash_password("Student@123"),
                role=UserRole.student,
                college_id=college_id
            )
            db.add(student_user)
            await db.flush()
            
            student = Student(
                roll_no=roll_no,
                name=full_name,
                dept_id=dept_map[dept_code],
                semester=random.randint(1, 8),
                phone=f"9{random.randint(100000000, 999999999)}",
                email=f"{roll_no.lower()}@student.edu",
                status=StudentStatus.active,
                user_id=student_user.id
            )
            db.add(student)
            await db.flush()
            student_list.append((student.id, dept_code))
        
        # 7. Create Timetable Slots
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        times = [("09:00", "10:30"), ("10:45", "12:15"), ("13:00", "14:30"), ("14:45", "16:15")]
        
        for dept_code in DEPARTMENTS:
            code = dept_code[1]
            subjects_in_dept = list(filter(lambda x: x[0].startswith(code), subject_map.keys()))
            
            for subject_code in subjects_in_dept[:5]:
                day = random.choice(days)
                start_time, end_time = random.choice(times)
                room = f"Room {random.randint(101, 304)}"
                
                slot = TimetableSlot(
                    day=day,
                    time_start=start_time,
                    time_end=end_time,
                    subject_id=subject_map[subject_code],
                    room=room,
                    semester=random.randint(1, 8),
                    dept_id=dept_map[code]
                )
                db.add(slot)
        
        # 8. Create Attendance Sessions and Records
        subjects_list = list(subject_map.items())
        
        for _ in range(20):
            subject_code, subject_id = random.choice(subjects_list)
            faculty_id = random.choice(faculty_list)
            session_date = datetime.utcnow() - timedelta(days=random.randint(1, 30))
            
            session = AttendanceSession(
                subject_id=subject_id,
                date=session_date,
                faculty_id=faculty_id,
                total_students=15
            )
            db.add(session)
            await db.flush()
            
            for student_id, student_dept in random.sample(student_list, min(15, len(student_list))):
                status = random.choice([AttendanceStatus.present, AttendanceStatus.absent, AttendanceStatus.late])
                record = AttendanceRecord(
                    session_id=session.id,
                    student_id=student_id,
                    status=status
                )
                db.add(record)
        
        # 9. Create Activities
        activity_list = []
        for title, activity_type in ACTIVITY_TYPES:
            activity_date = datetime.utcnow() + timedelta(days=random.randint(1, 30))
            dept_id = random.choice(list(dept_map.values()))
            activity = Activity(
                title=title,
                activity_type=ActivityType(activity_type),
                date=activity_date,
                description=f"Join us for {title}. This is a great opportunity to learn and network.",
                dept_id=dept_id,
                coordinator_id=random.choice(faculty_list),
                max_capacity=50,
                status=random.choice(list(ActivityStatus))
            )
            db.add(activity)
            await db.flush()
            activity_list.append(activity.id)
        
        # 10. Create Activity Enrollments
        for activity_id in activity_list:
            for student_id, _ in random.sample(student_list, random.randint(5, 15)):
                enrollment = ActivityEnrollment(
                    activity_id=activity_id,
                    student_id=student_id,
                    attended=random.choice([True, False])
                )
                db.add(enrollment)
        
        # 11. Create Alumni Records
        alumni_batches = list(range(2015, 2024))
        for _ in range(15):
            name = f"{random.choice(FIRST_NAMES_MALE + FIRST_NAMES_FEMALE)} {random.choice(LAST_NAMES)}"
            dept_id = random.choice(list(dept_map.values()))
            
            alumni = Alumni(
                name=name,
                batch_year=random.choice(alumni_batches),
                dept_id=dept_id,
                company=random.choice(COMPANIES),
                role=random.choice(["Software Engineer", "Data Scientist", "Product Manager", "Analyst"]),
                email=f"{name.lower().replace(' ', '.')}@company.com",
                linkedin=f"https://linkedin.com/in/{name.lower().replace(' ', '-')}",
                location=random.choice(["Bangalore", "Pune", "Mumbai", "Delhi", "Hyderabad", "Chennai"])
            )
            db.add(alumni)
        
        # 12. Learning content and quizzes
        learning_items = []
        for item in [
            {"title": "Introduction to Algebra", "subject": "Mathematics", "grade_level": 8, "content_type": LearningContentType.text, "body": "Algebra helps us represent unknown values using symbols.", "url": None, "dept_id": None},
            {"title": "HTML Basics", "subject": "Computer Science", "grade_level": 9, "content_type": LearningContentType.video, "body": None, "url": "https://www.youtube.com/watch?v=UB1O30fR-EE", "dept_id": dept_map["CSE"]},
            {"title": "Physics Notes: Motion", "subject": "Physics", "grade_level": 10, "content_type": LearningContentType.pdf, "body": "Download the notes and review formulas for speed, velocity, and acceleration.", "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "dept_id": None},
            {"title": "Chemistry Practice Quiz", "subject": "Chemistry", "grade_level": 11, "content_type": LearningContentType.quiz, "body": "Test your understanding of basic chemistry concepts.", "url": None, "dept_id": None},
            {"title": "English Grammar Essentials", "subject": "English", "grade_level": 7, "content_type": LearningContentType.text, "body": "Grammar improves clarity in communication and writing.", "url": None, "dept_id": None},
        ]:
            content = LearningContent(
                title=item["title"],
                subject=item["subject"],
                grade_level=item["grade_level"],
                content_type=item["content_type"],
                url=item["url"],
                body=item["body"],
                created_by=admin_id,
                dept_id=item["dept_id"],
            )
            db.add(content)
            await db.flush()
            learning_items.append(content)

        quiz_one = Quiz(title="HTML Basics Quiz", content_id=learning_items[1].id)
        db.add(quiz_one)
        await db.flush()
        for question, a, b, c, d, correct in [
            ("Which tag creates a hyperlink?", "<p>", "<a>", "<img>", "<div>", QuizCorrectOption.b),
            ("What does HTML stand for?", "Hyper Trainer Marking Language", "HyperText Markup Language", "High Text Machine Language", "None", QuizCorrectOption.b),
            ("Which element is used for the largest heading?", "<heading>", "<h6>", "<h1>", "<head>", QuizCorrectOption.c),
        ]:
            db.add(QuizQuestion(quiz_id=quiz_one.id, question=question, option_a=a, option_b=b, option_c=c, option_d=d, correct_option=correct))

        quiz_two = Quiz(title="Chemistry Quiz", content_id=learning_items[3].id)
        db.add(quiz_two)
        await db.flush()
        for question, a, b, c, d, correct in [
            ("What is the chemical symbol for water?", "H2O", "O2", "CO2", "NaCl", QuizCorrectOption.a),
            ("pH less than 7 indicates what?", "Neutral", "Acidic", "Basic", "Salty", QuizCorrectOption.b),
            ("Which particle has a positive charge?", "Electron", "Neutron", "Proton", "Photon", QuizCorrectOption.c),
        ]:
            db.add(QuizQuestion(quiz_id=quiz_two.id, question=question, option_a=a, option_b=b, option_c=c, option_d=d, correct_option=correct))

        # 13. Internships
        internship_data = [
            ("Software Engineering Intern", "BuildMate Tech", "Work on product features, APIs, and testing.", "Python, SQL, Git, APIs", 25000, 6, "Bangalore"),
            ("Civil Design Intern", "InfraWorks", "Support structural drawings and site planning.", "AutoCAD, Surveying, Structural Analysis", 18000, 4, "Hyderabad"),
            ("Mechanical Intern", "FabForge Industries", "Assist in manufacturing process improvements.", "CAD, Thermodynamics, Manufacturing", 16000, 5, "Pune"),
            ("Finance Analyst Intern", "CapitalLeaf", "Analyze reports and build financial models.", "Excel, Accounting, Financial Modeling", 22000, 3, "Mumbai"),
            ("Research Intern", "Quantum Lab", "Help with experiments, literature review, and analysis.", "Research Writing, Statistics, Critical Thinking", 20000, 6, "Delhi"),
        ]
        for title, company, description, skills_required, stipend, duration, location in internship_data:
            db.add(Internship(
                title=title,
                company=company,
                description=description,
                skills_required=skills_required,
                stipend=stipend,
                duration_months=duration,
                location=location,
                application_deadline=datetime.utcnow() + timedelta(days=30),
                posted_by=admin_id,
            ))

        # 14. Class sessions
        db.add(ClassSession(
            title="Data Structures Live Class",
            subject="Computer Science",
            faculty_id=faculty_list[0],
            dept_id=dept_map["CSE"],
            semester=3,
            meet_link="https://meet.google.com/demo-live-class",
            scheduled_at=datetime.utcnow() + timedelta(days=1),
            duration_minutes=90,
            status=SessionStatus.scheduled,
        ))
        db.add(ClassSession(
            title="Thermodynamics Revision",
            subject="Mechanical Engineering",
            faculty_id=faculty_list[2],
            dept_id=dept_map["MECH"],
            semester=5,
            meet_link="https://meet.google.com/demo-ended-class",
            scheduled_at=datetime.utcnow() - timedelta(days=1),
            duration_minutes=60,
            status=SessionStatus.ended,
        ))

        await db.commit()
        print("✓ Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_database())
