import os
import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select
from database import AsyncSessionLocal, init_db
from models import College, Department, User, Student, Subject, TimetableSlot, AttendanceSession, AttendanceRecord, Activity, ActivityEnrollment, Alumni
from models import (
    UserRole, AttendanceStatus, ActivityType, ActivityStatus, StudentStatus,
    Course, CourseModule, StudentCourseProgress, StudentModuleProgress, StudentXP, Quiz, QuizQuestion, QuizCorrectOption,
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
SEED_USER_PASSWORD = os.getenv("SEED_USER_PASSWORD", "change-me")

async def seed_all():
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
        
        # 3. Create Admin User from env vars
        admin_email = os.getenv("ADMIN_EMAIL", "")
        admin_password = os.getenv("ADMIN_PASSWORD", "")
        admin_name = os.getenv("ADMIN_NAME", "Admin")
        admin_id = None
        if not admin_email or not admin_password:
            print("WARNING: ADMIN_EMAIL or ADMIN_PASSWORD not set — skipping admin creation")
        else:
            existing = await db.execute(select(User).where(User.email == admin_email))
            admin = existing.scalars().first()
            if not admin:
                admin = User(
                    name=admin_name,
                    email=admin_email,
                    hashed_password=hash_password(admin_password),
                    role=UserRole.admin,
                    college_id=college_id,
                )
                db.add(admin)
                await db.flush()
                await db.commit()
                print(f"Admin created: {admin_email}")
            else:
                print(f"Admin already exists: {admin_email}")
            admin_id = admin.id

        # 4. Create Faculty Users
        faculty_list = []
        faculty_names = [
            ("Faculty 1", "faculty1@college.edu"),
            ("Faculty 2", "faculty2@college.edu"),
            ("Faculty 3", "faculty3@college.edu"),
            ("Faculty 4", "faculty4@college.edu"),
        ]

        for name, email in faculty_names:
            faculty = User(
                name=name,
                email=email,
                hashed_password=hash_password(SEED_USER_PASSWORD),
                role=UserRole.faculty,
                college_id=college_id
            )
            db.add(faculty)
            await db.flush()
            faculty_list.append(faculty.id)
        creator_id = admin_id or faculty_list[0]
        
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
                email=f"student{len(student_list) + 1:02d}@college.edu",
                hashed_password=hash_password(SEED_USER_PASSWORD),
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
                email=f"student{len(student_list) + 1:02d}@college.edu",
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
        
        # 12. Learning courses and quizzes
        course_one = Course(
            title="Python for Beginners",
            description=(
                "A structured introduction to Python programming for students starting from scratch.\n\n"
                "You will learn the syntax, data types, functions, loops, and how to build a small calculator project."
            ),
            subject="Computer Science",
            dept_id=dept_map["CSE"],
            semester=3,
            thumbnail_url="https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=1200&q=80",
            created_by=creator_id,
            is_published=True,
            xp_reward=150,
        )
        db.add(course_one)
        await db.flush()
        python_modules = [
            ("Introduction to Python", 1, None, None, (
                "Python is a beginner-friendly, high-level language used for web development, automation, data science, and AI.\n\n"
                "Install Python from python.org, verify the installation with `python --version`, and use a code editor like VS Code to start writing your first scripts."
            ), 10, 20),
            ("Variables and Data Types", 2, "https://www.youtube.com/watch?v=kqtD5dpn9C8", None, (
                "Variables store values so your program can reuse them later.\n\n"
                "Common data types include integers, strings, lists, and dictionaries. Use `int` for numbers, `str` for text, `list` for ordered collections, and `dict` for key-value data."
            ), 15, 20),
            ("Functions and Loops", 3, "https://www.youtube.com/watch?v=9Os0o3wzS_I", None, (
                "Functions help you package logic into reusable blocks, while loops let you repeat work until a condition changes.\n\n"
                "Together they let you write cleaner programs that are easier to test, debug, and reuse."
            ), 20, 25),
            ("Mini Project: Calculator", 4, None, None, (
                "Build a calculator that accepts two numbers and an operation, then prints the result.\n\n"
                "Use input handling, conditional statements, and functions to keep the code readable and reusable."
            ), 20, 30),
        ]
        for title, order_index, video_url, pdf_url, body, estimated_minutes, xp_reward in python_modules:
            db.add(CourseModule(
                course_id=course_one.id,
                title=title,
                order_index=order_index,
                video_url=video_url,
                pdf_url=pdf_url,
                body=body,
                estimated_minutes=estimated_minutes,
                xp_reward=xp_reward,
            ))
        await db.flush()
        python_quiz = Quiz(title="Python Basics Quiz", course_id=course_one.id)
        db.add(python_quiz)
        await db.flush()
        for question, a, b, c, d, correct in [
            ("Which keyword defines a function in Python?", "func", "define", "def", "lambda", QuizCorrectOption.c),
            ("What type is `[1, 2, 3]`?", "tuple", "list", "dict", "set", QuizCorrectOption.b),
            ("Which method adds an item to a list?", "append()", "add()", "push()", "insert()", QuizCorrectOption.a),
            ("What is the output of `2 ** 3`?", "5", "6", "8", "9", QuizCorrectOption.c),
        ]:
            db.add(QuizQuestion(quiz_id=python_quiz.id, question=question, option_a=a, option_b=b, option_c=c, option_d=d, correct_option=correct))

        course_two = Course(
            title="Engineering Mathematics Essentials",
            description=(
                "A compact course covering the mathematics students use repeatedly in engineering and problem solving.\n\n"
                "The lessons move from matrix operations to differentiation and integration with worked examples."
            ),
            subject="Mathematics",
            dept_id=None,
            semester=1,
            thumbnail_url="https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=1200&q=80",
            created_by=creator_id,
            is_published=True,
            xp_reward=120,
        )
        db.add(course_two)
        await db.flush()
        math_modules = [
            ("Matrix Operations", 1, "https://www.youtube.com/watch?v=xyAuNHPsq-g", None, "Matrices help represent and solve systems of linear equations and transformation problems.", 12, 20),
            ("Differentiation Basics", 2, "https://www.youtube.com/watch?v=WsQQvHm4lSw", None, "Differentiation measures how a function changes and forms the basis of optimization and motion problems.", 12, 20),
            ("Integration Introduction", 3, None, None, "Integration is the reverse of differentiation and helps calculate area, accumulation, and total change.", 12, 20),
        ]
        for title, order_index, video_url, pdf_url, body, estimated_minutes, xp_reward in math_modules:
            db.add(CourseModule(
                course_id=course_two.id,
                title=title,
                order_index=order_index,
                video_url=video_url,
                pdf_url=pdf_url,
                body=body,
                estimated_minutes=estimated_minutes,
                xp_reward=xp_reward,
            ))
        await db.flush()
        math_quiz = Quiz(title="Engineering Mathematics Quiz", course_id=course_two.id)
        db.add(math_quiz)
        await db.flush()
        for question, a, b, c, d, correct in [
            ("A square matrix has the same number of rows and columns.", "True", "False", "Only for 2x2 matrices", "Only for diagonal matrices", QuizCorrectOption.a),
            ("The derivative of a constant is", "1", "0", "The constant itself", "Undefined", QuizCorrectOption.b),
            ("Integration is commonly used to find", "Slope", "Area", "Temperature", "Probability", QuizCorrectOption.b),
        ]:
            db.add(QuizQuestion(quiz_id=math_quiz.id, question=question, option_a=a, option_b=b, option_c=c, option_d=d, correct_option=correct))

        # Seed a few real learning progress records for the new courses
        sample_students = student_list[:4]
        for idx, (student_id, _) in enumerate(sample_students):
            profile = StudentXP(student_id=student_id, total_xp=0, level=1, streak_days=0, badges="")
            db.add(profile)
            if idx == 0:
                course_progress = StudentCourseProgress(
                    student_id=student_id,
                    course_id=course_one.id,
                    modules_completed=4,
                    total_modules=4,
                    quiz_passed=True,
                    completed=True,
                    xp_earned=225,
                    started_at=datetime.utcnow() - timedelta(days=10),
                    last_activity=datetime.utcnow() - timedelta(days=1),
                    streak_days=7,
                )
                db.add(course_progress)
                await db.flush()
                for module in (await db.execute(select(CourseModule).where(CourseModule.course_id == course_one.id))).scalars().all():
                    db.add(StudentModuleProgress(student_id=student_id, module_id=module.id, completed=True, completed_at=datetime.utcnow() - timedelta(days=2)))
                profile.total_xp = 225
                profile.level = 2
                profile.streak_days = 7
                profile.last_activity_date = (datetime.utcnow() - timedelta(days=1)).date()
                profile.badges = "first_lesson,course_complete,streak_7"
            elif idx == 1:
                course_progress = StudentCourseProgress(
                    student_id=student_id,
                    course_id=course_one.id,
                    modules_completed=2,
                    total_modules=4,
                    quiz_passed=False,
                    completed=False,
                    xp_earned=40,
                    started_at=datetime.utcnow() - timedelta(days=4),
                    last_activity=datetime.utcnow() - timedelta(days=1),
                    streak_days=2,
                )
                db.add(course_progress)
                await db.flush()
                modules = (await db.execute(select(CourseModule).where(CourseModule.course_id == course_one.id).order_by(CourseModule.order_index))).scalars().all()
                for module in modules[:2]:
                    db.add(StudentModuleProgress(student_id=student_id, module_id=module.id, completed=True, completed_at=datetime.utcnow() - timedelta(days=1)))
                profile.total_xp = 40
                profile.level = 1
                profile.streak_days = 2
                profile.last_activity_date = (datetime.utcnow() - timedelta(days=1)).date()
            elif idx == 2:
                course_progress = StudentCourseProgress(
                    student_id=student_id,
                    course_id=course_two.id,
                    modules_completed=1,
                    total_modules=3,
                    quiz_passed=False,
                    completed=False,
                    xp_earned=20,
                    started_at=datetime.utcnow() - timedelta(days=3),
                    last_activity=datetime.utcnow(),
                    streak_days=1,
                )
                db.add(course_progress)
                await db.flush()
                first_module = (await db.execute(select(CourseModule).where(CourseModule.course_id == course_two.id).order_by(CourseModule.order_index))).scalars().first()
                if first_module:
                    db.add(StudentModuleProgress(student_id=student_id, module_id=first_module.id, completed=True, completed_at=datetime.utcnow()))
                profile.total_xp = 20
                profile.level = 1
                profile.streak_days = 1
                profile.last_activity_date = datetime.utcnow().date()
            else:
                course_progress = StudentCourseProgress(
                    student_id=student_id,
                    course_id=course_two.id,
                    modules_completed=0,
                    total_modules=3,
                    quiz_passed=False,
                    completed=False,
                    xp_earned=0,
                    started_at=datetime.utcnow() - timedelta(days=1),
                    last_activity=datetime.utcnow() - timedelta(days=1),
                    streak_days=1,
                )
                db.add(course_progress)
                profile.total_xp = 0
                profile.level = 1
                profile.streak_days = 1
                profile.last_activity_date = (datetime.utcnow() - timedelta(days=1)).date()

        # 13. Course-based learning hub content
        python_course = Course(
            title="Python for Beginners",
            description="A practical introduction to Python programming with hands-on lessons and a final mini project.",
            subject="Computer Science",
            dept_id=dept_map["CSE"],
            semester=3,
            thumbnail_url=None,
            created_by=creator_id,
            is_published=True,
            xp_reward=150,
        )
        db.add(python_course)
        await db.flush()

        python_modules = [
            {
                "title": "Introduction to Python",
                "body": "Python is a beginner-friendly programming language used for web development, data science, automation, and AI. It is readable, flexible, and supported by a huge ecosystem of libraries. To install Python, download it from python.org or use your system package manager, then verify the installation from your terminal with python --version or python3 --version.",
                "estimated_minutes": 10,
                "xp_reward": 20,
            },
            {
                "title": "Variables and Data Types",
                "body": "Variables store data that can change during a program. In Python, common data types include int for whole numbers, str for text, list for ordered collections, and dict for key-value pairs. Example: name = 'Asha', marks = 91, subjects = ['Math', 'CS'], profile = {'dept': 'CSE', 'semester': 3}.",
                "video_url": "https://www.youtube.com/watch?v=kqtD5dpn9C8",
                "estimated_minutes": 12,
                "xp_reward": 20,
            },
            {
                "title": "Functions and Loops",
                "body": "Functions let you package reusable logic into named blocks. Loops help you repeat tasks with for and while. Example:\n\ndef greet(name):\n    return f'Hello {name}'\n\nfor i in range(3):\n    print(greet(i))\n\nTogether, functions and loops are the backbone of clean Python programs.",
                "video_url": "https://www.youtube.com/watch?v=9Os0o3wzS_I",
                "estimated_minutes": 13,
                "xp_reward": 25,
            },
            {
                "title": "Mini Project: Calculator",
                "body": "Build a simple calculator that can add, subtract, multiply, and divide two numbers.\n\nStep 1: Ask the user for two inputs.\nStep 2: Ask which operation they want.\nStep 3: Use if/elif branches to perform the calculation.\nStep 4: Print the result and handle divide-by-zero safely.\n\nThis small project ties together variables, functions, conditionals, and input handling.",
                "estimated_minutes": 15,
                "xp_reward": 30,
            },
        ]

        for index, module_data in enumerate(python_modules, start=1):
            db.add(CourseModule(course_id=python_course.id, order_index=index, **module_data))

        python_quiz = Quiz(title="Python Basics Quiz", course_id=python_course.id)
        db.add(python_quiz)
        await db.flush()
        for question, a, b, c, d, correct in [
            ("Which function shows the version of Python?", "print()", "python --version", "pip install", "dir", QuizCorrectOption.b),
            ("Which type is best for storing multiple ordered items?", "dict", "set", "list", "int", QuizCorrectOption.c),
            ("What keyword defines a function?", "fun", "define", "def", "lambda", QuizCorrectOption.c),
            ("What does range(3) generate?", "0, 1, 2", "1, 2, 3", "0, 1, 2, 3", "3, 2, 1", QuizCorrectOption.a),
        ]:
            db.add(QuizQuestion(quiz_id=python_quiz.id, question=question, option_a=a, option_b=b, option_c=c, option_d=d, correct_option=correct))

        math_course = Course(
            title="Engineering Mathematics Essentials",
            description="Core mathematics topics for engineering students with quick lessons and practice questions.",
            subject="Mathematics",
            dept_id=None,
            semester=1,
            thumbnail_url=None,
            created_by=creator_id,
            is_published=True,
            xp_reward=120,
        )
        db.add(math_course)
        await db.flush()

        math_modules = [
            {
                "title": "Matrix Operations",
                "body": "Matrices help represent systems of equations, transformations, and data structures. Learn matrix addition, subtraction, multiplication, and transpose operations with simple worked examples.",
                "video_url": "https://www.youtube.com/watch?v=xyAuNHPsq-g",
                "estimated_minutes": 10,
                "xp_reward": 20,
            },
            {
                "title": "Differentiation Basics",
                "body": "Differentiation measures how a quantity changes. Understand derivatives of common functions, the power rule, and interpretation of slope in engineering contexts.",
                "video_url": "https://www.youtube.com/watch?v=WsQQvHm4lSw",
                "estimated_minutes": 10,
                "xp_reward": 20,
            },
            {
                "title": "Integration Introduction",
                "body": "Integration is the reverse of differentiation and is used to find area, accumulated change, and many physical quantities in engineering and science.",
                "estimated_minutes": 10,
                "xp_reward": 20,
            },
        ]

        for index, module_data in enumerate(math_modules, start=1):
            db.add(CourseModule(course_id=math_course.id, order_index=index, **module_data))

        math_quiz = Quiz(title="Engineering Mathematics Quiz", course_id=math_course.id)
        db.add(math_quiz)
        await db.flush()
        for question, a, b, c, d, correct in [
            ("What is the transpose of a matrix?", "Swap rows and columns", "Reverse numbers", "Multiply by 2", "Subtract diagonals", QuizCorrectOption.a),
            ("The derivative of x^2 is:", "x", "2x", "x^2", "1", QuizCorrectOption.b),
            ("Integration is commonly used to find:", "Slope", "Area", "Percentage", "Average height", QuizCorrectOption.b),
        ]:
            db.add(QuizQuestion(quiz_id=math_quiz.id, question=question, option_a=a, option_b=b, option_c=c, option_d=d, correct_option=correct))

        # 14. Internships
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
                posted_by=creator_id,
            ))

        # 15. Class sessions
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
    asyncio.run(seed_all())
