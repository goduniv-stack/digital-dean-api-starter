from uuid import UUID, uuid4
from fastapi import HTTPException, status
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate


class StudentRepository:
    def __init__(self):
        self._students: dict[UUID, StudentRead] = {}

    def clear(self):
        self._students.clear()

    def create(self, data: StudentCreate) -> StudentRead:
        for student in self._students.values():
            if student.email.lower() == data.email.lower():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Студент з таким email вже існує",
                )
        
        student_id = uuid4()
        student = StudentRead(id=student_id, **data.model_dump())
        self._students[student_id] = student
        return student

    def get_all(self, study_program: str | None = None) -> list[StudentRead]:
        students = list(self._students.values())
        if study_program:
            students = [s for s in students if s.study_program == study_program]
        return students

    def get_by_id(self, student_id: UUID) -> StudentRead:
        if student_id not in self._students:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Студента не знайдено",
            )
        return self._students[student_id]

    def update(self, student_id: UUID, data: StudentUpdate) -> StudentRead:
        current_student = self.get_by_id(student_id)
        
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Тіло оновлення не може бути порожнім",
            )

        if "email" in update_data:
            new_email = update_data["email"].lower()
            for s_id, s in self._students.items():
                if s_id != student_id and s.email.lower() == new_email:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Email вже використовується іншим студентом",
                    )

        updated_dict = current_student.model_dump()
        updated_dict.update(update_data)
        
        updated_student = StudentRead(**updated_dict)
        self._students[student_id] = updated_student
        return updated_student


repository = StudentRepository()