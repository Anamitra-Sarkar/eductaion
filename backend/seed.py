import os
import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select
from database import AsyncSessionLocal
from models import (
    College, Department, User, Student, Subject,
    TimetableSlot, AttendanceSession, AttendanceRecord,
    Activity, ActivityEnrollment, Alumni,
    UserRole, AttendanceStatus, ActivityType, ActivityStatus, StudentStatus,
    Course, CourseModule, StudentCourseProgress, StudentModuleProgress, StudentXP,
    Quiz, QuizQuestion, QuizCorrectOption,
    Internship, ClassSession, SessionStatus,
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
    ("Civil Engineering", "CIVIL"),
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
    ],
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

LEARNING_COURSES = [
    {
        "title": "GitHub Copilot CLI Essentials",
        "description": "Learn how an AI coding assistant can help you inspect code, search faster, and ship changes with confidence.",
        "subject": "AI Productivity",
        "dept_code": "CSE",
        "semester": 3,
        "thumbnail_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
        "xp_reward": 180,
        "modules": [
            ("What Copilot CLI Does", None, "Use an AI assistant to explore a codebase, summarize files, and accelerate routine engineering tasks.", 10, 25),
            ("Find the Right Files Fast", None, "Start by searching for the relevant symbols, routes, and components before editing anything.", 12, 25),
            ("Use Tools, Skills, and Subagents", None, "Break complex work into smaller actions and delegate when a specialized workflow is more efficient.", 15, 30),
            ("Verify Changes Before Shipping", None, "Run tests, inspect diffs, and confirm behavior on desktop and mobile before you commit.", 15, 30),
        ],
        "quiz": [
            ("What is the best first step before editing a large codebase?", "Search for relevant files", "Write code immediately", "Delete unused modules", "Skip context", QuizCorrectOption.a),
            ("What should you do after making an AI-assisted code change?", "Trust it blindly", "Run tests and review the diff", "Push immediately", "Ignore warnings", QuizCorrectOption.b),
            ("Why use a specialized workflow or subagent?", "To make tasks slower", "To avoid any context", "To handle focused work more efficiently", "To hide code", QuizCorrectOption.c),
            ("What is a good use of an AI coding assistant?", "Only generate code with no review", "Search, explain, and refine changes", "Replace all engineering judgment", "Skip validation", QuizCorrectOption.b),
        ],
    },
    {
        "title": "Prompting Better with AI Assistants",
        "description": "Build better prompts for coding and learning by adding context, constraints, and clear success criteria.",
        "subject": "Digital Skills",
        "dept_code": "CSE",
        "semester": 2,
        "thumbnail_url": "https://images.unsplash.com/photo-1516321497487-e288fb19713f?auto=format&fit=crop&w=1200&q=80",
        "xp_reward": 160,
        "modules": [
            ("Set the Goal", None, "State exactly what you want to achieve so the assistant can focus on the right outcome.", 10, 20),
            ("Add Constraints and Examples", None, "Mention formats, edge cases, and examples so the output matches your needs.", 12, 20),
            ("Ask for Structured Output", None, "Request tables, checklists, or step-by-step plans when clarity matters.", 12, 25),
            ("Refine, Review, Repeat", None, "Treat the assistant as a collaborator: review the result and iterate until it is useful.", 15, 30),
        ],
        "quiz": [
            ("What improves the quality of an AI response the most?", "Vague requests", "Clear context and constraints", "Longer typos", "No examples", QuizCorrectOption.b),
            ("Which request is most useful for a summary?", "Do something smart", "Give me a table with 3 columns", "Write anything", "Ignore the question", QuizCorrectOption.b),
            ("Why should you review AI output?", "Because it is always perfect", "To validate correctness and fit", "To avoid learning", "To make it longer", QuizCorrectOption.b),
            ("What is a good prompt habit?", "Start with the outcome you want", "Hide important details", "Assume the assistant knows everything", "Mix many unrelated tasks", QuizCorrectOption.a),
        ],
    },
]


async def seed_learning_content(db, college_id: int):
    dept_rows = (await db.execute(select(Department).where(Department.college_id == college_id))).scalars().all()
    dept_map = {dept.code: dept.id for dept in dept_rows}
    creator = (
        await db.execute(
            select(User)
            .where(User.college_id == college_id, User.role.in_([UserRole.admin, UserRole.faculty]))
            .order_by(User.id.asc())
        )
    ).scalars().first()
    if not creator:
        creator = (await db.execute(select(User).where(User.college_id == college_id).order_by(User.id.asc()))).scalars().first()
    if not creator:
        return

    existing_titles = set((await db.execute(select(Course.title))).scalars().all())
    for course_spec in LEARNING_COURSES:
        if course_spec["title"] in existing_titles:
            continue
        dept_id = dept_map.get(course_spec["dept_code"])
        course = Course(
            title=course_spec["title"],
            description=course_spec["description"],
            subject=course_spec["subject"],
            dept_id=dept_id,
            semester=course_spec["semester"],
            thumbnail_url=course_spec["thumbnail_url"],
            created_by=creator.id,
            is_published=True,
            xp_reward=course_spec["xp_reward"],
        )
        db.add(course)
        await db.flush()
        for order_index, (title, video_url, body, estimated_minutes, xp_reward) in enumerate(course_spec["modules"], start=1):
            db.add(CourseModule(
                course_id=course.id,
                title=title,
                order_index=order_index,
                video_url=video_url,
                body=body,
                estimated_minutes=estimated_minutes,
                xp_reward=xp_reward,
            ))
        await db.flush()
        quiz = Quiz(title=f"{course_spec['title']} Quiz", course_id=course.id)
        db.add(quiz)
        await db.flush()
        for question, a, b, c, d, correct in course_spec["quiz"]:
            db.add(QuizQuestion(
                quiz_id=quiz.id,
                question=question,
                option_a=a,
                option_b=b,
                option_c=c,
                option_d=d,
                correct_option=correct,
            ))


async def seed_all():
    async with AsyncSessionLocal() as db:
        # --- Idempotency guard: skip if college already exists ---
        existing_college = (await db.execute(
            select(College).where(College.name == "Institute of Technology Excellence")
        )).scalars().first()
        if existing_college:
            print("Seed data already present — ensuring learning content exists.")
            await seed_learning_content(db, existing_college.id)
            await db.commit()
            return

        # 1. College
        college = College(
            name="Institute of Technology Excellence",
            address="123 Campus Road, Bangalore, India",
            naac_grade="A+",
            principal="Dr. A.K. Sharma",
            academic_year="2024-2025",
            domain="student.edu",
        )
        db.add(college)
        await db.flush()
        college_id = college.id

        # 2. Departments
        dept_map = {}
        for name, code in DEPARTMENTS:
            dept = Department(name=name, code=code, college_id=college_id)
            db.add(dept)
            await db.flush()
            dept_map[code] = dept.id

        # 3. Admin user
        admin_email = os.getenv("ADMIN_EMAIL", "")
        admin_password = os.getenv("ADMIN_PASSWORD", "")
        admin_name = os.getenv("ADMIN_NAME", "Admin")
        admin_id = None
        if not admin_email or not admin_password:
            print("WARNING: ADMIN_EMAIL or ADMIN_PASSWORD not set — skipping admin creation")
        else:
            existing = (await db.execute(select(User).where(User.email == admin_email))).scalars().first()
            if not existing:
                admin = User(
                    name=admin_name,
                    email=admin_email,
                    hashed_password=hash_password(admin_password),
                    role=UserRole.admin,
                    college_id=college_id,
                )
                db.add(admin)
                await db.flush()
                admin_id = admin.id
                print(f"Admin created: {admin_email}")
            else:
                admin_id = existing.id
                print(f"Admin already exists: {admin_email}")

        # 4. Faculty
        faculty_list = []
        for name, email in [
            ("Faculty 1", "faculty1@college.edu"),
            ("Faculty 2", "faculty2@college.edu"),
            ("Faculty 3", "faculty3@college.edu"),
            ("Faculty 4", "faculty4@college.edu"),
        ]:
            faculty = User(
                name=name,
                email=email,
                hashed_password=hash_password(SEED_USER_PASSWORD),
                role=UserRole.faculty,
                college_id=college_id,
            )
            db.add(faculty)
            await db.flush()
            faculty_list.append(faculty.id)
        creator_id = admin_id or faculty_list[0]

        # 5. Subjects
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
                    credit_hours=credits,
                )
                db.add(subject)
                await db.flush()
                subject_map[code] = subject.id
                faculty_idx += 1

        # 6. Students
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
            idx = len(student_list)
            student_user = User(
                name=full_name,
                email=f"student{idx + 1:02d}@college.edu",
                hashed_password=hash_password(SEED_USER_PASSWORD),
                role=UserRole.student,
                college_id=college_id,
            )
            db.add(student_user)
            await db.flush()
            student = Student(
                roll_no=roll_no,
                name=full_name,
                dept_id=dept_map[dept_code],
                semester=random.randint(1, 8),
                phone=f"9{random.randint(100000000, 999999999)}",
                email=f"student{idx + 1:02d}@college.edu",
                status=StudentStatus.active,
                user_id=student_user.id,
            )
            db.add(student)
            await db.flush()
            student_list.append((student.id, dept_code))

        # 7. Timetable
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        times = [("09:00", "10:30"), ("10:45", "12:15"), ("13:00", "14:30"), ("14:45", "16:15")]
        for dept_name, code in DEPARTMENTS:
            subjects_in_dept = [k for k in subject_map if k.startswith(code)]
            for subject_code in subjects_in_dept[:5]:
                start_time, end_time = random.choice(times)
                db.add(TimetableSlot(
                    day=random.choice(days),
                    time_start=start_time,
                    time_end=end_time,
                    subject_id=subject_map[subject_code],
                    room=f"Room {random.randint(101, 304)}",
                    semester=random.randint(1, 8),
                    dept_id=dept_map[code],
                ))

        # 8. Attendance
        subjects_list = list(subject_map.items())
        for _ in range(20):
            subject_code, subject_id = random.choice(subjects_list)
            session = AttendanceSession(
                subject_id=subject_id,
                date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                faculty_id=random.choice(faculty_list),
                total_students=15,
            )
            db.add(session)
            await db.flush()
            for student_id, _ in random.sample(student_list, min(15, len(student_list))):
                db.add(AttendanceRecord(
                    session_id=session.id,
                    student_id=student_id,
                    status=random.choice([AttendanceStatus.present, AttendanceStatus.absent, AttendanceStatus.late]),
                ))

        # 9. Activities
        activity_list = []
        for title, activity_type in ACTIVITY_TYPES:
            activity = Activity(
                title=title,
                activity_type=ActivityType(activity_type),
                date=datetime.utcnow() + timedelta(days=random.randint(1, 30)),
                description=f"Join us for {title}.",
                dept_id=random.choice(list(dept_map.values())),
                coordinator_id=random.choice(faculty_list),
                max_capacity=50,
                status=random.choice(list(ActivityStatus)),
            )
            db.add(activity)
            await db.flush()
            activity_list.append(activity.id)

        # 10. Activity enrollments
        for activity_id in activity_list:
            for student_id, _ in random.sample(student_list, random.randint(5, 15)):
                db.add(ActivityEnrollment(
                    activity_id=activity_id,
                    student_id=student_id,
                    attended=random.choice([True, False]),
                ))

        # 11. Alumni
        for _ in range(15):
            name = f"{random.choice(FIRST_NAMES_MALE + FIRST_NAMES_FEMALE)} {random.choice(LAST_NAMES)}"
            db.add(Alumni(
                name=name,
                batch_year=random.choice(list(range(2015, 2024))),
                dept_id=random.choice(list(dept_map.values())),
                company=random.choice(COMPANIES),
                role=random.choice(["Software Engineer", "Data Scientist", "Product Manager", "Analyst"]),
                email=f"{name.lower().replace(' ', '.')}_{random.randint(1,9999)}@company.com",
                linkedin=f"https://linkedin.com/in/{name.lower().replace(' ', '-')}",
                location=random.choice(["Bangalore", "Pune", "Mumbai", "Delhi", "Hyderabad", "Chennai"]),
            ))

        # 12. Courses (each title seeded exactly once)
        course_one = Course(
            title="Python for Beginners",
            description="A structured introduction to Python programming for students starting from scratch.",
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
        for order_index, (title, video_url, body, estimated_minutes, xp_reward) in enumerate([
            ("Introduction to Python", None,
             "Python is a beginner-friendly, high-level language used for web development, automation, data science, and AI.", 10, 20),
            ("Variables and Data Types", "https://www.youtube.com/watch?v=kqtD5dpn9C8",
             "Variables store values. Common types: int, str, list, dict.", 15, 20),
            ("Functions and Loops", "https://www.youtube.com/watch?v=9Os0o3wzS_I",
             "Functions package reusable logic; loops repeat work until a condition changes.", 20, 25),
            ("Mini Project: Calculator", None,
             "Build a calculator using input handling, conditionals, and functions.", 20, 30),
        ], start=1):
            db.add(CourseModule(
                course_id=course_one.id, title=title, order_index=order_index,
                video_url=video_url, body=body,
                estimated_minutes=estimated_minutes, xp_reward=xp_reward,
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
            db.add(QuizQuestion(quiz_id=python_quiz.id, question=question,
                                option_a=a, option_b=b, option_c=c, option_d=d, correct_option=correct))

        course_two = Course(
            title="Engineering Mathematics Essentials",
            description="Core mathematics topics for engineering students with quick lessons and practice questions.",
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
        for order_index, (title, video_url, body, estimated_minutes, xp_reward) in enumerate([
            ("Matrix Operations", "https://www.youtube.com/watch?v=xyAuNHPsq-g",
             "Matrices help represent systems of equations and transformations.", 12, 20),
            ("Differentiation Basics", "https://www.youtube.com/watch?v=WsQQvHm4lSw",
             "Differentiation measures how a function changes.", 12, 20),
            ("Integration Introduction", None,
             "Integration is the reverse of differentiation and is used to find area.", 12, 20),
        ], start=1):
            db.add(CourseModule(
                course_id=course_two.id, title=title, order_index=order_index,
                video_url=video_url, body=body,
                estimated_minutes=estimated_minutes, xp_reward=xp_reward,
            ))
        await db.flush()
        math_quiz = Quiz(title="Engineering Mathematics Quiz", course_id=course_two.id)
        db.add(math_quiz)
        await db.flush()
        for question, a, b, c, d, correct in [
            ("A square matrix has the same number of rows and columns.", "True", "False", "Only for 2x2", "Only diagonal", QuizCorrectOption.a),
            ("The derivative of a constant is", "1", "0", "The constant", "Undefined", QuizCorrectOption.b),
            ("Integration is commonly used to find", "Slope", "Area", "Temperature", "Probability", QuizCorrectOption.b),
        ]:
            db.add(QuizQuestion(quiz_id=math_quiz.id, question=question,
                                option_a=a, option_b=b, option_c=c, option_d=d, correct_option=correct))

        # 13. Student XP + progress
        sample_students = student_list[:4]
        for idx, (student_id, _) in enumerate(sample_students):
            profile = StudentXP(student_id=student_id, total_xp=0, level=1, streak_days=0, badges="")
            db.add(profile)
            if idx == 0:
                cp = StudentCourseProgress(
                    student_id=student_id, course_id=course_one.id,
                    modules_completed=4, total_modules=4, quiz_passed=True,
                    completed=True, xp_earned=225,
                    started_at=datetime.utcnow() - timedelta(days=10),
                    last_activity=datetime.utcnow() - timedelta(days=1), streak_days=7,
                )
                db.add(cp)
                await db.flush()
                modules = (await db.execute(
                    select(CourseModule).where(CourseModule.course_id == course_one.id)
                )).scalars().all()
                for m in modules:
                    db.add(StudentModuleProgress(
                        student_id=student_id, module_id=m.id,
                        completed=True, completed_at=datetime.utcnow() - timedelta(days=2),
                    ))
                profile.total_xp = 225
                profile.level = 2
                profile.streak_days = 7
                profile.last_activity_date = (datetime.utcnow() - timedelta(days=1)).date()
                profile.badges = "first_lesson,course_complete,streak_7"
            elif idx == 1:
                cp = StudentCourseProgress(
                    student_id=student_id, course_id=course_one.id,
                    modules_completed=2, total_modules=4, quiz_passed=False,
                    completed=False, xp_earned=40,
                    started_at=datetime.utcnow() - timedelta(days=4),
                    last_activity=datetime.utcnow() - timedelta(days=1), streak_days=2,
                )
                db.add(cp)
                await db.flush()
                modules = (await db.execute(
                    select(CourseModule).where(CourseModule.course_id == course_one.id)
                    .order_by(CourseModule.order_index)
                )).scalars().all()
                for m in modules[:2]:
                    db.add(StudentModuleProgress(
                        student_id=student_id, module_id=m.id,
                        completed=True, completed_at=datetime.utcnow() - timedelta(days=1),
                    ))
                profile.total_xp = 40
                profile.streak_days = 2
                profile.last_activity_date = (datetime.utcnow() - timedelta(days=1)).date()
            elif idx == 2:
                cp = StudentCourseProgress(
                    student_id=student_id, course_id=course_two.id,
                    modules_completed=1, total_modules=3, quiz_passed=False,
                    completed=False, xp_earned=20,
                    started_at=datetime.utcnow() - timedelta(days=3),
                    last_activity=datetime.utcnow(), streak_days=1,
                )
                db.add(cp)
                await db.flush()
                first_module = (await db.execute(
                    select(CourseModule).where(CourseModule.course_id == course_two.id)
                    .order_by(CourseModule.order_index)
                )).scalars().first()
                if first_module:
                    db.add(StudentModuleProgress(
                        student_id=student_id, module_id=first_module.id,
                        completed=True, completed_at=datetime.utcnow(),
                    ))
                profile.total_xp = 20
                profile.streak_days = 1
                profile.last_activity_date = datetime.utcnow().date()
            else:
                cp = StudentCourseProgress(
                    student_id=student_id, course_id=course_two.id,
                    modules_completed=0, total_modules=3, quiz_passed=False,
                    completed=False, xp_earned=0,
                    started_at=datetime.utcnow() - timedelta(days=1),
                    last_activity=datetime.utcnow() - timedelta(days=1), streak_days=1,
                )
                db.add(cp)
                profile.streak_days = 1
                profile.last_activity_date = (datetime.utcnow() - timedelta(days=1)).date()

        # 14. Internships
        for title, company, description, skills_required, stipend, duration, location in [
            ("Software Engineering Intern", "BuildMate Tech", "Work on product features, APIs, and testing.",
             "Python, SQL, Git, APIs", 25000, 6, "Bangalore"),
            ("Civil Design Intern", "InfraWorks", "Support structural drawings and site planning.",
             "AutoCAD, Surveying, Structural Analysis", 18000, 4, "Hyderabad"),
            ("Mechanical Intern", "FabForge Industries", "Assist in manufacturing process improvements.",
             "CAD, Thermodynamics, Manufacturing", 16000, 5, "Pune"),
            ("Finance Analyst Intern", "CapitalLeaf", "Analyze reports and build financial models.",
             "Excel, Accounting, Financial Modeling", 22000, 3, "Mumbai"),
            ("Research Intern", "Quantum Lab", "Help with experiments, literature review, and analysis.",
             "Research Writing, Statistics, Critical Thinking", 20000, 6, "Delhi"),
        ]:
            db.add(Internship(
                title=title, company=company, description=description,
                skills_required=skills_required, stipend=stipend,
                duration_months=duration, location=location,
                application_deadline=datetime.utcnow() + timedelta(days=30),
                posted_by=creator_id,
            ))

        # 15. Class sessions
        db.add(ClassSession(
            title="Data Structures Live Class", subject="Computer Science",
            faculty_id=faculty_list[0], dept_id=dept_map["CSE"],
            semester=3, meet_link="https://meet.google.com/demo-live-class",
            scheduled_at=datetime.utcnow() + timedelta(days=1),
            duration_minutes=90, status=SessionStatus.scheduled,
        ))
        db.add(ClassSession(
            title="Thermodynamics Revision", subject="Mechanical Engineering",
            faculty_id=faculty_list[2], dept_id=dept_map["MECH"],
            semester=5, meet_link="https://meet.google.com/demo-ended-class",
            scheduled_at=datetime.utcnow() - timedelta(days=1),
            duration_minutes=60, status=SessionStatus.ended,
        ))

        await seed_learning_content(db, college_id)
        await db.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_all())
