from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
import re

from database import get_db
from models import CareerProfile, Student, User, UserRole
from schemas import CareerProfileUpdate, CareerProfileOut
from routers.auth import get_current_user

router = APIRouter(prefix="/career", tags=["career"])

CAREER_MAP = {
    "software engineer": {
        "required_skills": ["Python", "Data Structures", "Algorithms", "Git", "SQL"],
        "recommended_certifications": [
            {"title": "Google Associate Cloud Engineer", "url": "https://cloud.google.com/certification"},
            {"title": "AWS Certified Developer", "url": "https://aws.amazon.com/certification"},
            {"title": "Meta Back-End Developer (Coursera)", "url": "https://www.coursera.org/professional-certificates/meta-back-end-developer"},
        ],
        "job_boards": [
            {"title": "LinkedIn Jobs", "url": "https://linkedin.com/jobs"},
            {"title": "Naukri", "url": "https://naukri.com"},
            {"title": "Internshala", "url": "https://internshala.com"},
        ],
    },
    "data scientist": {
        "required_skills": ["Python", "Statistics", "Machine Learning", "SQL", "Pandas"],
        "recommended_certifications": [
            {"title": "Google Data Analytics", "url": "https://www.coursera.org/professional-certificates/google-data-analytics"},
            {"title": "IBM Data Science", "url": "https://www.coursera.org/professional-certificates/ibm-data-science"},
        ],
        "job_boards": [
            {"title": "LinkedIn Jobs", "url": "https://linkedin.com/jobs"},
            {"title": "Indeed", "url": "https://in.indeed.com"},
        ],
    },
    "product manager": {
        "required_skills": ["Product Thinking", "Roadmapping", "Analytics", "Communication", "Stakeholder Management"],
        "recommended_certifications": [
            {"title": "AIPMM Certified Product Manager", "url": "https://www.aipmm.com/certification"},
            {"title": "Google Project Management", "url": "https://www.coursera.org/professional-certificates/google-project-management"},
        ],
        "job_boards": [
            {"title": "LinkedIn Jobs", "url": "https://linkedin.com/jobs"},
            {"title": "Wellfound", "url": "https://wellfound.com/jobs"},
        ],
    },
    "civil engineer": {
        "required_skills": ["AutoCAD", "Surveying", "Structural Analysis", "Estimating", "Project Management"],
        "recommended_certifications": [
            {"title": "AutoCAD Certification", "url": "https://www.autodesk.com/certification"},
            {"title": "Primavera P6", "url": "https://www.oracle.com/industries/construction-engineering/primavera-p6/"},
        ],
        "job_boards": [
            {"title": "Naukri", "url": "https://naukri.com"},
            {"title": "Shine", "url": "https://www.shine.com"},
        ],
    },
    "mechanical engineer": {
        "required_skills": ["Thermodynamics", "CAD", "Manufacturing", "Mechanics", "Quality Control"],
        "recommended_certifications": [
            {"title": "SolidWorks Certification", "url": "https://www.solidworks.com/certification"},
            {"title": "Six Sigma Yellow Belt", "url": "https://www.goleansixsigma.com"},
        ],
        "job_boards": [
            {"title": "LinkedIn Jobs", "url": "https://linkedin.com/jobs"},
            {"title": "Naukri", "url": "https://naukri.com"},
        ],
    },
    "electronics engineer": {
        "required_skills": ["Analog Circuits", "Digital Electronics", "Embedded Systems", "PCB Design", "C Programming"],
        "recommended_certifications": [
            {"title": "Altium Designer Certification", "url": "https://www.altium.com/certification"},
            {"title": "NVIDIA Deep Learning Institute", "url": "https://www.nvidia.com/en-us/training/"},
        ],
        "job_boards": [
            {"title": "LinkedIn Jobs", "url": "https://linkedin.com/jobs"},
            {"title": "Indeed", "url": "https://in.indeed.com"},
        ],
    },
    "finance/mba": {
        "required_skills": ["Excel", "Financial Modeling", "Accounting", "Presentation", "Business Analysis"],
        "recommended_certifications": [
            {"title": "CFA Institute", "url": "https://www.cfainstitute.org/"},
            {"title": "Google Data Analytics", "url": "https://www.coursera.org/professional-certificates/google-data-analytics"},
        ],
        "job_boards": [
            {"title": "LinkedIn Jobs", "url": "https://linkedin.com/jobs"},
            {"title": "Naukri", "url": "https://naukri.com"},
        ],
    },
    "research/phd": {
        "required_skills": ["Research Writing", "Statistics", "Literature Review", "Critical Thinking", "Experiment Design"],
        "recommended_certifications": [
            {"title": "Elsevier Researcher Academy", "url": "https://researcheracademy.elsevier.com/"},
            {"title": "Academic Writing", "url": "https://www.edx.org/learn/writing"},
        ],
        "job_boards": [
            {"title": "Scholarship Positions", "url": "https://scholarshippositions.com/"},
            {"title": "PhDPortal", "url": "https://www.phdportal.com/"},
        ],
    },
    "government/upsc": {
        "required_skills": ["Current Affairs", "Essay Writing", "General Studies", "Reasoning", "Public Administration"],
        "recommended_certifications": [
            {"title": "Free UPSC Prep Notes", "url": "https://upsc.gov.in/"},
            {"title": "NPTEL Public Policy", "url": "https://nptel.ac.in/"},
        ],
        "job_boards": [
            {"title": "Employment News", "url": "https://employmentnews.gov.in/"},
            {"title": "Government Jobs", "url": "https://www.sarkariresult.com/"},
        ],
    },
    "entrepreneur": {
        "required_skills": ["Problem Solving", "Marketing", "Sales", "Finance", "Execution"],
        "recommended_certifications": [
            {"title": "Y Combinator Startup School", "url": "https://www.startupschool.org/"},
            {"title": "Wharton Entrepreneurship", "url": "https://www.coursera.org/specializations/wharton-entrepreneurship"},
        ],
        "job_boards": [
            {"title": "Wellfound", "url": "https://wellfound.com/jobs"},
            {"title": "AngelList", "url": "https://wellfound.com/"},
        ],
    },
}

ROLE_DISPLAY_NAMES = {
    "software engineer": "Software Engineer",
    "data scientist": "Data Scientist",
    "product manager": "Product Manager",
    "civil engineer": "Civil Engineer",
    "mechanical engineer": "Mechanical Engineer",
    "electronics engineer": "Electronics Engineer",
    "finance/mba": "Finance/MBA",
    "research/phd": "Research/PhD",
    "government/upsc": "Government/UPSC",
    "entrepreneur": "Entrepreneur",
}

CAREER_RESOURCES = [
    {"title": "CS50 by Harvard", "url": "https://cs50.harvard.edu/x/", "type": "course", "tags": ["programming", "computer science", "beginners"]},
    {"title": "The Missing Semester of Your CS Education", "url": "https://missing.csail.mit.edu/", "type": "course", "tags": ["tools", "terminal", "git"]},
    {"title": "fast.ai — Practical Deep Learning", "url": "https://course.fast.ai/", "type": "course", "tags": ["AI", "machine learning", "deep learning"]},
    {"title": "freeCodeCamp", "url": "https://www.freecodecamp.org/", "type": "course", "tags": ["web development", "javascript", "free"]},
    {"title": "NPTEL Online Courses", "url": "https://nptel.ac.in/", "type": "course", "tags": ["engineering", "IIT", "India", "free"]},
    {"title": "Swayam Portal", "url": "https://swayam.gov.in/", "type": "course", "tags": ["government", "India", "free", "certification"]},
    {"title": "Khan Academy", "url": "https://www.khanacademy.org/", "type": "course", "tags": ["maths", "science", "free", "rural"]},
    {"title": "MIT OpenCourseWare", "url": "https://ocw.mit.edu/", "type": "course", "tags": ["engineering", "science", "free"]},
    {"title": "The Pragmatic Programmer (Book)", "url": "https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/", "type": "book", "tags": ["programming", "career", "software engineering"]},
    {"title": "Clean Code by Robert Martin (Book)", "url": "https://www.amazon.in/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882", "type": "book", "tags": ["programming", "best practices"]},
    {"title": "Cracking the Coding Interview (Book)", "url": "https://www.crackingthecodinginterview.com/", "type": "book", "tags": ["interviews", "algorithms", "placement"]},
    {"title": "3Blue1Brown — Math & ML Videos", "url": "https://www.youtube.com/@3blue1brown", "type": "video", "tags": ["maths", "AI", "visual learning"]},
    {"title": "Fireship — Web Dev Videos", "url": "https://www.youtube.com/@Fireship", "type": "video", "tags": ["web development", "javascript", "fast"]},
    {"title": "Kunal Kushwaha DSA Course (YouTube)", "url": "https://www.youtube.com/watch?v=rZ41y93P2Qo", "type": "video", "tags": ["DSA", "Java", "placement", "India"]},
    {"title": "Apna College (YouTube)", "url": "https://www.youtube.com/@ApnaCollegeOfficial", "type": "video", "tags": ["DSA", "placement", "India", "Hindi"]},
    {"title": "LeetCode", "url": "https://leetcode.com/", "type": "tool", "tags": ["DSA", "interviews", "practice", "placement"]},
    {"title": "GeeksforGeeks", "url": "https://www.geeksforgeeks.org/", "type": "tool", "tags": ["DSA", "placement", "India", "reference"]},
    {"title": "Excalidraw — System Design Diagrams", "url": "https://excalidraw.com/", "type": "tool", "tags": ["system design", "interviews", "diagrams"]},
    {"title": "PM Internship Scheme Portal", "url": "https://pminternship.mca.gov.in/", "type": "tool", "tags": ["internship", "government", "India", "PM scheme"]},
    {"title": "Internshala", "url": "https://internshala.com/", "type": "tool", "tags": ["internship", "jobs", "India", "students"]},
    {"title": "Google Scholar", "url": "https://scholar.google.com/", "type": "tool", "tags": ["research", "papers", "citations"]},
]


def _split_csv(value: str) -> List[str]:
    return [item.strip() for item in re.split(r"[,\n;]+", value or "") if item.strip()]


def _match_role(target_role: str) -> Optional[str]:
    role = (target_role or "").strip().lower()
    if not role:
        return None
    aliases = {
        "software engineer": ["software engineer", "developer", "backend", "frontend", "full stack"],
        "data scientist": ["data scientist", "data science", "machine learning", "ml engineer", "ai engineer"],
        "product manager": ["product manager", "pm"],
        "civil engineer": ["civil engineer"],
        "mechanical engineer": ["mechanical engineer"],
        "electronics engineer": ["electronics engineer", "electrical engineer", "ece"],
        "finance/mba": ["finance", "mba", "investment banking", "analyst"],
        "research/phd": ["research", "phd", "ph.d", "academic"],
        "government/upsc": ["government", "upsc", "civil services", "ias", "ips"],
        "entrepreneur": ["entrepreneur", "startup", "founder"],
    }
    for key, candidates in aliases.items():
        if any(candidate in role for candidate in candidates):
            return key
    return role if role in CAREER_MAP else None


@router.get("/profile", response_model=CareerProfileOut)
async def get_profile(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Student access required")
    student_result = await db.execute(select(Student).where(Student.user_id == current_user.id))
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    result = await db.execute(select(CareerProfile).where(CareerProfile.student_id == student.id))
    profile = result.scalars().first()
    if not profile:
        profile = CareerProfile(student_id=student.id, interests="", skills="", target_role="", target_companies="")
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    return profile


@router.put("/profile", response_model=CareerProfileOut)
async def update_profile(
    payload: CareerProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Student access required")
    student_result = await db.execute(select(Student).where(Student.user_id == current_user.id))
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    result = await db.execute(select(CareerProfile).where(CareerProfile.student_id == student.id))
    profile = result.scalars().first()
    if not profile:
        profile = CareerProfile(student_id=student.id)
        db.add(profile)
    profile.interests = payload.interests
    profile.skills = payload.skills
    profile.target_role = payload.target_role
    profile.target_companies = payload.target_companies
    await db.commit()
    await db.refresh(profile)
    return profile


@router.get("/advice")
async def get_advice(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Student access required")
    student_result = await db.execute(select(Student).where(Student.user_id == current_user.id))
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    result = await db.execute(select(CareerProfile).where(CareerProfile.student_id == student.id))
    profile = result.scalars().first()
    if not profile or not profile.target_role.strip():
        return {"error": "complete_profile", "message": "Please complete your career profile first to get personalized advice."}
    matched_key = _match_role(profile.target_role)
    if not matched_key:
        return {"error": "complete_profile", "message": "Please complete your career profile first to get personalized advice."}
    data = CAREER_MAP[matched_key]
    student_skills = {item.lower() for item in _split_csv(profile.skills)}
    skills_analysis = [{"skill": skill, "has": skill.lower() in student_skills} for skill in data["required_skills"]]
    missing_skills_count = sum(1 for item in skills_analysis if not item["has"])
    filled_fields = sum(1 for value in [profile.interests, profile.skills, profile.target_role, profile.target_companies] if str(value).strip())
    profile_completion = int((filled_fields / 4) * 100)
    return {
        "matched_role": ROLE_DISPLAY_NAMES.get(matched_key, matched_key.title()),
        "skills_analysis": skills_analysis,
        "recommended_certifications": data["recommended_certifications"],
        "job_boards": data["job_boards"],
        "missing_skills_count": missing_skills_count,
        "profile_completion": profile_completion,
    }


@router.get("/resources")
async def get_resources():
    return CAREER_RESOURCES


@router.get("/profiles")
async def list_profiles(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    result = await db.execute(select(CareerProfile))
    profiles = result.scalars().all()
    student_ids = {profile.student_id for profile in profiles}
    student_map = {}
    if student_ids:
        student_result = await db.execute(select(Student).where(Student.id.in_(student_ids)))
        student_map = {student.id: student.name for student in student_result.scalars().all()}
    return [
        {
            "student_id": profile.student_id,
            "student_name": student_map.get(profile.student_id),
            "target_role": profile.target_role,
        }
        for profile in profiles
    ]
