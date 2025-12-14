import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from main import app
from database import get_session
from models import Student, StudentCreate

DATABASE_URL = "sqlite:///test.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(name="client")
def client_fixture():
    import os
    if os.path.exists("test.db"):
        os.remove("test.db")
    SQLModel.metadata.create_all(engine)
    with TestClient(app) as client:
        yield client
    SQLModel.metadata.drop_all(engine)
    engine.dispose()  # Close all connections
    if os.path.exists("test.db"):
        os.remove("test.db")


def test_get_all_students(client: TestClient):
    with Session(engine) as session:
        student = Student(name="Test Student", age=25, email="test@example.com")
        session.add(student)
        session.commit()

    response = client.get("/students")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Test Student"

def test_get_student(client: TestClient):
    with Session(engine) as session:
        student = Student(name="Test Student", age=25, email="test@example.com")
        session.add(student)
        session.commit()
        session.refresh(student)

    response = client.get(f"/students/{student.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Student"

def test_get_student_not_found(client: TestClient):
    response = client.get("/students/99")
    assert response.status_code == 404

def test_create_student(client: TestClient):
    new_student_data = {"name": "New Student", "age": 30, "email": "new@example.com"}
    response = client.post("/students", json=new_student_data)
    assert response.status_code == 200
    created_student = response.json()
    assert "id" in created_student
    assert created_student["name"] == new_student_data["name"]

    with Session(engine) as session:
        student_in_db = session.get(Student, created_student["id"])
        assert student_in_db is not None
        assert student_in_db.name == new_student_data["name"]

def test_update_student(client: TestClient):
    with Session(engine) as session:
        student = Student(name="Test Student", age=25, email="test@example.com")
        session.add(student)
        session.commit()
        session.refresh(student)
    
    updated_data = {"name": "Updated Name", "age": 30, "email": "updated@example.com"}
    response = client.put(f"/students/{student.id}", json=updated_data)
    assert response.status_code == 200
    updated_student = response.json()
    assert updated_student["name"] == updated_data["name"]
    assert updated_student["age"] == updated_data["age"]

    with Session(engine) as session:
        student_in_db = session.get(Student, student.id)
        assert student_in_db is not None
        assert student_in_db.name == updated_data["name"]

def test_update_student_not_found(client: TestClient):
    updated_data = {"name": "Updated Name", "age": 30, "email": "updated@example.com"}
    response = client.put("/students/99", json=updated_data)
    assert response.status_code == 404

def test_delete_student(client: TestClient):
    with Session(engine) as session:
        student = Student(name="Test Student", age=25, email="test@example.com")
        session.add(student)
        session.commit()
        session.refresh(student)

    response = client.delete(f"/students/{student.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Student deleted successfully"}

    with Session(engine) as session:
        student_in_db = session.get(Student, student.id)
        assert student_in_db is None

def test_delete_student_not_found(client: TestClient):
    response = client.delete("/students/99")
    assert response.status_code == 404
