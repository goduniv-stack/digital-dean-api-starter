from uuid import UUID
from fastapi import APIRouter, status
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate
from app.repositories.student_repository import repository

router = APIRouter(prefix="/api/v1/students", tags=["students"])


@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate):
    return repository.create(payload)


@router.get("", response_model=list[StudentRead])
def get_students(study_program: str | None = None):
    return repository.get_all(study_program=study_program)


@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: UUID):
    return repository.get_by_id(student_id)


@router.patch("/{student_id}", response_model=StudentRead)
def update_student(student_id: UUID, payload: StudentUpdate):
    return repository.update(student_id, payload)