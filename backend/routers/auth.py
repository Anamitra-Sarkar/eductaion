from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from typing import List
import os
from passlib.context import CryptContext
from jose import JWTError, jwt
from database import get_db
from schemas import UserCreate, UserLogin, Token, User as UserSchema, FacultyCreate
from models import User, College, UserRole

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserSchema)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Hard-reject non-students
    if user.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Self-registration is only allowed for students")
    
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Fetch college and validate email domain
    result = await db.execute(select(College).where(College.id == user.college_id))
    college = result.scalars().first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    
    # Validate email domain matches college domain
    if not user.email.endswith(f"@{college.domain}"):
        raise HTTPException(status_code=400, detail=f"Email must use your institution's official domain")
    
    # Force role to student (don't trust client)
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=UserRole.student,
        college_id=user.college_id
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login(form_data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form_data.email))
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserSchema)
async def get_me(current_user: User = Depends(get_current_user)):
      return current_user

@router.post("/register/faculty", response_model=UserSchema)
async def register_faculty(
    faculty: FacultyCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify admin
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only administrators can create faculty accounts")
    
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == faculty.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create faculty user in same college as admin
    db_user = User(
        name=faculty.name,
        email=faculty.email,
        hashed_password=hash_password(faculty.password),
        role=UserRole.faculty,
        college_id=current_user.college_id
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
