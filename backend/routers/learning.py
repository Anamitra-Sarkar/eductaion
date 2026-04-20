from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_db
from models import (
    BADGES,
    XP_PER_LEVEL,
    Course,
    CourseModule,
    Quiz,
    QuizAttempt,
    QuizQuestion,
    Student,
    StudentCourseProgress,
    StudentModuleProgress,
    StudentXP,
    User,
    UserRole,
    level_for_xp,
)
from routers.auth import get_current_user
from schemas import (
    CourseCreate,
    CourseModuleCreate,
    CourseModuleUpdate,
    CourseUpdate,
    CourseOut,
    QuizAttemptCreate,
    QuizCreate,
)

router = APIRouter(prefix="/learning", tags=["learning"])


def _is_staff(user: User) -> bool:
    return user.role in {UserRole.admin, UserRole.faculty}


def _is_admin(user: User) -> bool:
    return user.role == UserRole.admin


def _badge_payload(key: str, earned: bool = False) -> Dict[str, Any]:
    badge = BADGES[key]
    return {
        "key": key,
        "name": badge["name"],
        "icon": badge["icon"],
        "description": badge["description"],
        "xp_threshold": badge.get("xp_threshold"),
        "earned": earned,
    }


def _badge_keys(raw: Optional[str]) -> List[str]:
    return [key for key in (raw or "").split(",") if key]


def _store_badges(profile: StudentXP, keys: List[str]) -> None:
    profile.badges = ",".join(sorted(dict.fromkeys(keys)))


def _has_badge(profile: StudentXP, key: str) -> bool:
    return key in _badge_keys(profile.badges)


def _module_progress_payload(module: CourseModule, completed: bool = False, completed_at: Optional[datetime] = None):
    return {
        "id": module.id,
        "title": module.title,
        "order_index": module.order_index,
        "video_url": module.video_url,
        "pdf_url": module.pdf_url,
        "body": module.body,
        "estimated_minutes": module.estimated_minutes,
        "xp_reward": module.xp_reward,
        "completed": completed,
        "completed_at": completed_at,
    }


async def _get_student(db: AsyncSession, user_id: int) -> Student:
    result = await db.execute(select(Student).where(Student.user_id == user_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student


async def _get_or_create_xp(db: AsyncSession, student_id: int) -> StudentXP:
    result = await db.execute(select(StudentXP).where(StudentXP.student_id == student_id))
    profile = result.scalars().first()
    if profile:
        return profile
    profile = StudentXP(student_id=student_id)
    db.add(profile)
    await db.flush()
    return profile


async def _get_course_progress(db: AsyncSession, student_id: int, course_id: int) -> Optional[StudentCourseProgress]:
    result = await db.execute(
        select(StudentCourseProgress).where(
            StudentCourseProgress.student_id == student_id,
            StudentCourseProgress.course_id == course_id,
        )
    )
    return result.scalars().first()


async def _course_has_quiz(db: AsyncSession, course_id: int) -> bool:
    result = await db.execute(select(Quiz.id).where(Quiz.course_id == course_id))
    return result.first() is not None


def _update_xp_level(profile: StudentXP) -> None:
    profile.level = level_for_xp(profile.total_xp)


async def _apply_streak(profile: StudentXP) -> bool:
    today = date.today()
    yesterday = today - timedelta(days=1)
    previous = profile.last_activity_date
    if previous == today:
        return False
    if previous == yesterday:
        profile.streak_days += 1
    else:
        profile.streak_days = 1
    profile.last_activity_date = today
    return True


async def _maybe_award_badges(
    db: AsyncSession,
    profile: StudentXP,
    student: Student,
    *,
    first_lesson: bool = False,
    quiz_passed: bool = False,
    top_score: bool = False,
    course_completed: bool = False,
) -> List[Dict[str, Any]]:
    earned: List[Dict[str, Any]] = []
    badges = set(_badge_keys(profile.badges))

    if first_lesson and "first_lesson" not in badges:
        badges.add("first_lesson")
        earned.append(_badge_payload("first_lesson", True))

    if course_completed and "course_complete" not in badges:
        badges.add("course_complete")
        earned.append(_badge_payload("course_complete", True))

    if top_score and "top_scorer" not in badges:
        badges.add("top_scorer")
        earned.append(_badge_payload("top_scorer", True))

    if profile.streak_days >= 7 and "streak_7" not in badges:
        badges.add("streak_7")
        earned.append(_badge_payload("streak_7", True))

    if quiz_passed:
        passed = await db.execute(
            select(func.count(StudentCourseProgress.id)).where(
                StudentCourseProgress.student_id == student.id,
                StudentCourseProgress.quiz_passed.is_(True),
            )
        )
        if int(passed.scalar() or 0) >= 5 and "quiz_master" not in badges:
            badges.add("quiz_master")
            earned.append(_badge_payload("quiz_master", True))

    enrollments = await db.execute(
        select(func.count(StudentCourseProgress.id)).where(StudentCourseProgress.student_id == student.id)
    )
    if int(enrollments.scalar() or 0) >= 3 and "explorer" not in badges:
        badges.add("explorer")
        earned.append(_badge_payload("explorer", True))

    _store_badges(profile, list(badges))
    return earned


async def _course_summary(db: AsyncSession, course: Course) -> Dict[str, Any]:
    module_count = len(course.modules)
    progress_rows = (
        await db.execute(select(StudentCourseProgress).where(StudentCourseProgress.course_id == course.id))
    ).scalars().all()
    enrolled_count = len(progress_rows)
    avg_completion_pct = 0.0
    if progress_rows:
        avg_completion_pct = round(
            sum(
                (row.modules_completed / row.total_modules * 100)
                if row.total_modules
                else 0
                for row in progress_rows
            )
            / len(progress_rows),
            1,
        )
    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "subject": course.subject,
        "semester": course.semester,
        "thumbnail_url": course.thumbnail_url,
        "is_published": course.is_published,
        "created_by": course.created_by,
        "created_at": course.created_at,
        "xp_reward": course.xp_reward,
        "module_count": module_count,
        "enrolled_count": enrolled_count,
        "avg_completion_pct": avg_completion_pct,
    }


async def _course_detail_payload(
    db: AsyncSession,
    course: Course,
    current_user: Optional[User] = None,
) -> Dict[str, Any]:
    student_progress: Optional[StudentCourseProgress] = None
    module_progress: Dict[int, StudentModuleProgress] = {}
    quiz_payload: Optional[Dict[str, Any]] = None
    enrolled = False
    completion_pct = 0.0
    if current_user and current_user.role == UserRole.student:
        student = await _get_student(db, current_user.id)
        student_progress = await _get_course_progress(db, student.id, course.id)
        if student_progress:
            enrolled = True
            completion_pct = round(
                (student_progress.modules_completed / student_progress.total_modules * 100)
                if student_progress.total_modules
                else 0,
                1,
            )
            results = await db.execute(
                select(StudentModuleProgress).where(StudentModuleProgress.student_id == student.id)
            )
            module_progress = {row.module_id: row for row in results.scalars().all()}

    if course.quiz:
        questions = []
        for question in course.quiz.questions:
            payload = {
                "id": question.id,
                "question": question.question,
                "option_a": question.option_a,
                "option_b": question.option_b,
                "option_c": question.option_c,
                "option_d": question.option_d,
            }
            if current_user and current_user.role == UserRole.admin:
                payload["correct_option"] = question.correct_option
            questions.append(payload)
        quiz_payload = {
            "id": course.quiz.id,
            "title": course.quiz.title,
            "questions": questions,
        }

    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "subject": course.subject,
        "semester": course.semester,
        "thumbnail_url": course.thumbnail_url,
        "dept_id": course.dept_id,
        "is_published": course.is_published,
        "xp_reward": course.xp_reward,
        "module_count": len(course.modules),
        "enrolled": enrolled,
        "completion_pct": completion_pct,
        "modules": [
            {
                **_module_progress_payload(
                    module,
                    completed=bool(module_progress.get(module.id) and module_progress[module.id].completed),
                    completed_at=module_progress.get(module.id).completed_at if module_progress.get(module.id) else None,
                )
            }
            for module in course.modules
        ],
        "quiz": quiz_payload,
        "progress": {
            "modules_completed": student_progress.modules_completed if student_progress else 0,
            "total_modules": student_progress.total_modules if student_progress else len(course.modules),
            "quiz_passed": student_progress.quiz_passed if student_progress else False,
            "completed": student_progress.completed if student_progress else False,
            "xp_earned": student_progress.xp_earned if student_progress else 0,
            "streak_days": student_progress.streak_days if student_progress else 0,
        } if student_progress else None,
    }


@router.get("/courses", response_model=List[CourseOut])
async def list_courses(
    subject: Optional[str] = None,
    semester: Optional[int] = None,
    dept_id: Optional[int] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Course)
        .options(selectinload(Course.modules))
        .where(Course.is_published.is_(True))
        .order_by(Course.created_at.desc())
    )
    courses = result.scalars().unique().all()
    if subject:
        courses = [course for course in courses if course.subject.lower() == subject.lower()]
    if semester is not None:
        courses = [course for course in courses if course.semester == semester]
    if dept_id is not None:
        courses = [course for course in courses if course.dept_id == dept_id]
    if search:
        needle = search.lower()
        courses = [
            course for course in courses
            if needle in course.title.lower() or needle in course.description.lower() or needle in course.subject.lower()
        ]
    return [await _course_summary(db, course) for course in courses]


@router.post("/courses")
async def create_course(course: CourseCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not _is_staff(current_user):
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    record = Course(
        title=course.title,
        description=course.description,
        subject=course.subject,
        dept_id=course.dept_id,
        semester=course.semester,
        thumbnail_url=course.thumbnail_url,
        created_by=current_user.id,
        is_published=course.is_published,
        xp_reward=course.xp_reward,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return await _course_summary(db, record)


@router.get("/courses/{course_id}")
async def get_course(course_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Course)
        .options(selectinload(Course.modules), selectinload(Course.quiz).selectinload(Quiz.questions))
        .where(Course.id == course_id)
    )
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if not course.is_published and current_user.role == UserRole.student:
        raise HTTPException(status_code=403, detail="Course is not published")
    if current_user.role == UserRole.student:
        student = await _get_student(db, current_user.id)
        progress = await _get_course_progress(db, student.id, course.id)
        if not course.is_published and not progress:
            raise HTTPException(status_code=403, detail="Course is not published")
    return await _course_detail_payload(db, course, current_user)


@router.put("/courses/{course_id}")
async def update_course(course_id: int, course_update: CourseUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if not _is_staff(current_user):
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    if current_user.role == UserRole.faculty and course.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own course")
    for field in ["title", "description", "subject", "dept_id", "semester", "thumbnail_url", "xp_reward", "is_published"]:
        value = getattr(course_update, field)
        if value is not None:
            setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return await _course_summary(db, course)


@router.delete("/courses/{course_id}")
async def delete_course(course_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if not _is_staff(current_user):
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    if current_user.role == UserRole.faculty and course.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own course")
    await db.delete(course)
    await db.commit()
    return {"message": "Course deleted"}


@router.post("/courses/{course_id}/publish")
async def publish_course(course_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if not _is_staff(current_user):
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    if current_user.role == UserRole.faculty and course.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only publish your own course")
    course.is_published = True
    await db.commit()
    await db.refresh(course)
    return await _course_summary(db, course)


@router.post("/courses/{course_id}/enroll")
async def enroll_course(course_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Student access required")
    student = await _get_student(db, current_user.id)
    result = await db.execute(
        select(Course).options(selectinload(Course.modules)).where(Course.id == course_id)
    )
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if not course.is_published:
        raise HTTPException(status_code=403, detail="Course is not published")
    progress = await _get_course_progress(db, student.id, course.id)
    if progress:
        return {
            "course_id": course.id,
            "student_id": student.id,
            "enrolled": True,
            "total_modules": progress.total_modules,
            "modules_completed": progress.modules_completed,
            "quiz_passed": progress.quiz_passed,
            "completed": progress.completed,
        }
    progress = StudentCourseProgress(
        student_id=student.id,
        course_id=course.id,
        total_modules=len(course.modules),
        modules_completed=0,
        quiz_passed=False,
        completed=False,
        xp_earned=0,
        started_at=datetime.utcnow(),
        last_activity=datetime.utcnow(),
        streak_days=0,
    )
    db.add(progress)
    await db.flush()
    xp = await _get_or_create_xp(db, student.id)
    earned = await _maybe_award_badges(db, xp, student, course_completed=False)
    _update_xp_level(xp)
    await db.commit()
    return {
        "course_id": course.id,
        "student_id": student.id,
        "enrolled": True,
        "total_modules": progress.total_modules,
        "modules_completed": progress.modules_completed,
        "quiz_passed": progress.quiz_passed,
        "completed": progress.completed,
        "badges_earned": earned,
    }


@router.post("/courses/{course_id}/modules")
async def add_module(course_id: int, module: CourseModuleCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not _is_staff(current_user):
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    result = await db.execute(select(Course).options(selectinload(Course.modules)).where(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role == UserRole.faculty and course.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own course")
    order_index = module.order_index or ((course.modules[-1].order_index if course.modules else 0) + 1)
    record = CourseModule(
        course_id=course.id,
        title=module.title,
        order_index=order_index,
        video_url=module.video_url,
        pdf_url=module.pdf_url,
        body=module.body,
        estimated_minutes=module.estimated_minutes,
        xp_reward=module.xp_reward,
    )
    db.add(record)
    await db.flush()
    for progress in (await db.execute(select(StudentCourseProgress).where(StudentCourseProgress.course_id == course.id))).scalars().all():
        progress.total_modules = len(course.modules) + 1
    await db.commit()
    await db.refresh(record)
    return _module_progress_payload(record)


@router.put("/modules/{module_id}")
async def update_module(module_id: int, module_update: CourseModuleUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not _is_staff(current_user):
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    if current_user.role == UserRole.faculty and module.course.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own course")
    result = await db.execute(
        select(CourseModule).options(selectinload(CourseModule.course)).where(CourseModule.id == module_id)
    )
    module = result.scalars().first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    for field in ["title", "order_index", "video_url", "pdf_url", "body", "estimated_minutes", "xp_reward"]:
        value = getattr(module_update, field)
        if value is not None:
            setattr(module, field, value)
    await db.commit()
    await db.refresh(module)
    return _module_progress_payload(module)


@router.delete("/modules/{module_id}")
async def delete_module(module_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not _is_staff(current_user):
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    if current_user.role == UserRole.faculty and module.course.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own course")
    result = await db.execute(
        select(CourseModule).options(selectinload(CourseModule.course)).where(CourseModule.id == module_id)
    )
    module = result.scalars().first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    course_id = module.course_id
    await db.delete(module)
    await db.flush()
    remaining = (await db.execute(select(func.count(CourseModule.id)).where(CourseModule.course_id == course_id))).scalar() or 0
    for progress in (await db.execute(select(StudentCourseProgress).where(StudentCourseProgress.course_id == course_id))).scalars().all():
        progress.total_modules = int(remaining)
        progress.modules_completed = min(progress.modules_completed, int(remaining))
    await db.commit()
    return {"message": "Module deleted"}


@router.post("/modules/{module_id}/complete")
async def complete_module(module_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Student access required")
    student = await _get_student(db, current_user.id)
    result = await db.execute(
        select(CourseModule)
        .options(selectinload(CourseModule.course))
        .where(CourseModule.id == module_id)
    )
    module = result.scalars().first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    progress = await _get_course_progress(db, student.id, module.course_id)
    if not progress:
        raise HTTPException(status_code=400, detail="Enroll in the course first")
    module_progress = await db.execute(
        select(StudentModuleProgress).where(
            StudentModuleProgress.student_id == student.id,
            StudentModuleProgress.module_id == module.id,
        )
    )
    module_row = module_progress.scalars().first()
    if module_row and module_row.completed:
        xp = await _get_or_create_xp(db, student.id)
        return {
            "xp_earned": 0,
            "new_total_xp": xp.total_xp,
            "level": xp.level,
            "badges_earned": [],
            "course_completed": progress.completed,
        }
    if not module_row:
        module_row = StudentModuleProgress(student_id=student.id, module_id=module.id, completed=False)
        db.add(module_row)
        await db.flush()
    module_row.completed = True
    module_row.completed_at = datetime.utcnow()
    progress.modules_completed = min(progress.total_modules, progress.modules_completed + 1)
    progress.last_activity = datetime.utcnow()

    xp = await _get_or_create_xp(db, student.id)
    prev_level = xp.level
    module_xp = int(module.xp_reward)
    xp.total_xp += module_xp
    _update_xp_level(xp)
    await _apply_streak(xp)
    progress.streak_days = xp.streak_days
    progress.xp_earned += module_xp

    total_completed_modules = await db.execute(
        select(func.count(StudentModuleProgress.id)).where(
            StudentModuleProgress.student_id == student.id,
            StudentModuleProgress.completed.is_(True),
        )
    )
    badges_earned = await _maybe_award_badges(
        db,
        xp,
        student,
        first_lesson=int(total_completed_modules.scalar() or 0) == 1,
        course_completed=False,
    )

    course_completed = False
    quiz_exists = await _course_has_quiz(db, module.course_id)
    if progress.modules_completed >= progress.total_modules and (progress.quiz_passed or not quiz_exists):
        if not progress.completed:
            progress.completed = True
            progress.xp_earned += module.course.xp_reward
            xp.total_xp += module.course.xp_reward
            _update_xp_level(xp)
            course_completed = True
            badges_earned += await _maybe_award_badges(db, xp, student, course_completed=True)

    if xp.level > prev_level:
        badges_earned = badges_earned

    await db.commit()
    return {
        "xp_earned": module_xp + (module.course.xp_reward if course_completed else 0),
        "new_total_xp": xp.total_xp,
        "level": xp.level,
        "badges_earned": badges_earned,
        "course_completed": course_completed,
    }


@router.post("/courses/{course_id}/quiz")
async def create_course_quiz(course_id: int, quiz: QuizCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).options(selectinload(Course.quiz)).where(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if not _is_staff(current_user):
        raise HTTPException(status_code=403, detail="Faculty or admin access required")
    if current_user.role == UserRole.faculty and course.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own course")
    if course.quiz:
        await db.delete(course.quiz)
        await db.flush()
    quiz_record = Quiz(title=quiz.title or f"{course.title} Quiz", course_id=course.id)
    db.add(quiz_record)
    await db.flush()
    for question in quiz.questions:
        db.add(
            QuizQuestion(
                quiz_id=quiz_record.id,
                question=question.question,
                option_a=question.option_a,
                option_b=question.option_b,
                option_c=question.option_c,
                option_d=question.option_d,
                correct_option=question.correct_option,
            )
        )
    await db.commit()
    return {"id": quiz_record.id, "title": quiz_record.title, "question_count": len(quiz.questions)}


@router.get("/courses/{course_id}/quiz")
async def get_course_quiz(course_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Quiz).options(selectinload(Quiz.questions)).where(Quiz.course_id == course_id)
    )
    quiz = result.scalars().first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    questions = []
    for question in quiz.questions:
        payload = {
            "id": question.id,
            "question": question.question,
            "option_a": question.option_a,
            "option_b": question.option_b,
            "option_c": question.option_c,
            "option_d": question.option_d,
        }
        if current_user.role in {UserRole.admin, UserRole.faculty}:
            payload["correct_option"] = question.correct_option
        questions.append(payload)
    return {"id": quiz.id, "title": quiz.title, "questions": questions}


@router.post("/courses/{course_id}/quiz/attempt")
async def attempt_course_quiz(course_id: int, attempt: QuizAttemptCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Student access required")
    student = await _get_student(db, current_user.id)
    course_result = await db.execute(
        select(Course).options(selectinload(Course.quiz).selectinload(Quiz.questions), selectinload(Course.modules)).where(Course.id == course_id)
    )
    course = course_result.scalars().first()
    if not course or not course.quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    progress = await _get_course_progress(db, student.id, course.id)
    if not progress:
        raise HTTPException(status_code=400, detail="Enroll in the course first")
    answers = {item.question_id: item.answer.lower().strip() for item in attempt.answers}
    correct_count = 0
    correct_answers: List[Dict[str, Any]] = []
    for question in course.quiz.questions:
        expected = question.correct_option.value
        selected = answers.get(question.id, "")
        correct_answers.append(
            {
                "question_id": question.id,
                "question": question.question,
                "selected": selected,
                "correct_option": expected,
                "correct_answer": getattr(question, f"option_{expected}"),
                "is_correct": selected == expected,
            }
        )
        if selected == expected:
            correct_count += 1
    score = round((correct_count / len(course.quiz.questions)) * 100, 1) if course.quiz.questions else 0.0
    passed = score >= 60
    attempt_record = QuizAttempt(quiz_id=course.quiz.id, student_id=student.id, score=score, attempted_at=datetime.utcnow())
    db.add(attempt_record)

    xp = await _get_or_create_xp(db, student.id)
    base_xp = 25 if passed else 0
    badges_earned: List[Dict[str, Any]] = []
    prev_level = xp.level
    if passed and not progress.quiz_passed:
        progress.quiz_passed = True
        progress.xp_earned += base_xp
        xp.total_xp += base_xp
        _update_xp_level(xp)
        await db.flush()
        badges_earned = await _maybe_award_badges(db, xp, student, quiz_passed=True, top_score=score == 100)
    elif passed and progress.quiz_passed:
        if score == 100:
            badges_earned = await _maybe_award_badges(db, xp, student, top_score=True)
    course_completed_now = False
    if progress.modules_completed >= progress.total_modules and progress.quiz_passed and not progress.completed:
        progress.completed = True
        progress.xp_earned += course.xp_reward
        xp.total_xp += course.xp_reward
        _update_xp_level(xp)
        badges_earned += await _maybe_award_badges(db, xp, student, course_completed=True)
        course_completed_now = True
    if xp.level > prev_level:
        progress.last_activity = datetime.utcnow()
    await db.commit()
    return {
        "score": score,
        "passed": passed,
        "xp_earned": base_xp + (course.xp_reward if course_completed_now else 0),
        "badges_earned": badges_earned,
        "correct_answers": correct_answers,
    }


@router.get("/leaderboard")
async def leaderboard(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    rows = await db.execute(
        select(Student, StudentXP)
        .join(User, User.id == Student.user_id)
        .outerjoin(StudentXP, StudentXP.student_id == Student.id)
        .where(User.role == UserRole.student)
        .order_by(func.coalesce(StudentXP.total_xp, 0).desc(), Student.name.asc())
        .limit(10)
    )
    entries = []
    for index, (student, xp) in enumerate(rows.all(), start=1):
        profile = xp or StudentXP(student_id=student.id, total_xp=0, level=1, streak_days=0, badges="")
        entries.append(
            {
                "rank": index,
                "student_name": student.name,
                "xp": profile.total_xp,
                "level": profile.level or level_for_xp(profile.total_xp),
                "badges_count": len(_badge_keys(profile.badges)),
                "streak": profile.streak_days,
            }
        )
    return entries


@router.get("/my-progress")
async def my_progress(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Student access required")
    student = await _get_student(db, current_user.id)
    xp = await _get_or_create_xp(db, student.id)
    progress_rows = (
        await db.execute(
            select(StudentCourseProgress, Course)
            .join(Course, Course.id == StudentCourseProgress.course_id)
            .where(StudentCourseProgress.student_id == student.id)
            .order_by(Course.created_at.desc())
        )
    ).all()
    courses = []
    for progress, course in progress_rows:
        completion_pct = round((progress.modules_completed / progress.total_modules * 100) if progress.total_modules else 0, 1)
        courses.append(
            {
                "course_id": course.id,
                "id": course.id,
                "course_name": course.title,
                "title": course.title,
                "modules_completed": progress.modules_completed,
                "modules_done": progress.modules_completed,
                "total_modules": progress.total_modules,
                "quiz_passed": progress.quiz_passed,
                "completed": progress.completed,
                "xp_earned": progress.xp_earned,
                "completion_pct": completion_pct,
            }
        )
    earned_keys = set(_badge_keys(xp.badges))
    badges = [_badge_payload(key, key in earned_keys) for key in BADGES.keys()]
    return {
        "total_xp": xp.total_xp,
        "level": xp.level,
        "streak_days": xp.streak_days,
        "streak": xp.streak_days,
        "badges": badges,
        "courses": courses,
        "enrolled_courses": courses,
    }


@router.get("/xp-info")
async def xp_info():
    return {
        "badges": BADGES,
        "xp_per_level": XP_PER_LEVEL,
        "level_formula": "floor(total_xp / 200) + 1",
    }
