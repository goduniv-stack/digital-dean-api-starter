import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.student_repository import repository

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_repo():
    repository.clear()


def test_create_student():
    response = client.post(
        "/api/v1/students",
        json={
            "full_name": "Олена Коваль",
            "email": "olena.koval@example.com",
            "group_code": "КН-31",
            "study_program": "Комп'ютерні науки",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == "olena.koval@example.com"


def test_invalid_email():
    response = client.post(
        "/api/v1/students",
        json={
            "full_name": "Олена Коваль",
            "email": "not-an-email",
            "group_code": "КН-31",
            "study_program": "Комп'ютерні науки",
        },
    )
    assert response.status_code == 422


def test_get_students_list():
    client.post(
        "/api/v1/students",
        json={
            "full_name": "Олена Коваль",
            "email": "olena.koval@example.com",
            "group_code": "КН-31",
            "study_program": "Комп'ютерні науки",
        },
    )
    response = client.get("/api/v1/students")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_unknown_field_rejected():
    response = client.post(
        "/api/v1/students",
        json={
            "full_name": "Олена Коваль",
            "email": "olena.koval@example.com",
            "group_code": "КН-31",
            "study_program": "Комп'ютерні науки",
            "is_admin": True,
        },
    )
    assert response.status_code == 422