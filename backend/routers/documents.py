from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from hashlib import sha256
from datetime import datetime

from database import get_db
from models import DocumentVerification, Student, User, UserRole, DocumentType
from schemas import DocumentOut
from routers.auth import get_current_user

router = APIRouter(prefix="/documents", tags=["documents"])


def _document_payload(document: DocumentVerification, student_name: Optional[str] = None, verifier_name: Optional[str] = None):
    return {
        "id": document.id,
        "student_id": document.student_id,
        "document_type": document.document_type,
        "filename": document.filename,
        "hash": document.hash,
        "verified": document.verified,
        "verified_by": document.verified_by,
        "submitted_at": document.submitted_at,
        "verified_at": document.verified_at,
        "student_name": student_name,
        "verified_by_name": verifier_name,
    }


async def _verification_result(db: AsyncSession, document: Optional[DocumentVerification]):
    if not document or not document.verified:
        return {"valid": False, "document_type": None, "student_name": None, "verified_at": None}
    student_result = await db.execute(select(Student).where(Student.id == document.student_id))
    student = student_result.scalars().first()
    return {
        "valid": True,
        "document_type": document.document_type,
        "student_name": student.name if student else "Unknown",
        "verified_at": document.verified_at.isoformat() if document.verified_at else None,
    }


@router.post("/upload", response_model=DocumentOut)
async def upload_document(
    file: UploadFile = File(...),
    document_type: DocumentType = Form(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Student access required")
    student_result = await db.execute(select(Student).where(Student.user_id == current_user.id))
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    file_bytes = await file.read()
    file_hash = sha256(file_bytes).hexdigest()
    document = DocumentVerification(
        student_id=student.id,
        document_type=document_type,
        filename=file.filename or "uploaded-file",
        hash=file_hash,
        verified=False,
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)
    return _document_payload(document, student.name)


@router.get("/my", response_model=List[DocumentOut])
async def my_documents(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Student access required")
    student_result = await db.execute(select(Student).where(Student.user_id == current_user.id))
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    result = await db.execute(select(DocumentVerification).where(DocumentVerification.student_id == student.id))
    docs = result.scalars().all()
    return [_document_payload(doc, student.name) for doc in docs]


@router.get("")
async def all_documents(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    result = await db.execute(select(DocumentVerification))
    docs = result.scalars().all()
    student_ids = {doc.student_id for doc in docs}
    verifier_ids = {doc.verified_by for doc in docs if doc.verified_by}
    students = {}
    verifiers = {}
    if student_ids:
        student_result = await db.execute(select(Student).where(Student.id.in_(student_ids)))
        students = {s.id: s.name for s in student_result.scalars().all()}
    if verifier_ids:
        verifier_result = await db.execute(select(User).where(User.id.in_(verifier_ids)))
        verifiers = {u.id: u.name for u in verifier_result.scalars().all()}
    return [_document_payload(doc, students.get(doc.student_id), verifiers.get(doc.verified_by)) for doc in docs]


@router.get("/verify-hash")
async def verify_hash_public(hash: str = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DocumentVerification).where(DocumentVerification.hash == hash))
    document = result.scalars().first()
    return await _verification_result(db, document)


@router.get("/{id}/check/{hash}")
async def verify_hash_by_path(id: int, hash: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DocumentVerification).where(DocumentVerification.hash == hash))
    document = result.scalars().first()
    return await _verification_result(db, document)


@router.put("/{id}/verify")
async def verify_document(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    result = await db.execute(select(DocumentVerification).where(DocumentVerification.id == id))
    document = result.scalars().first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    document.verified = True
    document.verified_by = current_user.id
    document.verified_at = datetime.utcnow()
    await db.commit()
    await db.refresh(document)
    return _document_payload(document)
