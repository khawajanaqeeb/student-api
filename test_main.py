from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_students():
    response = client.get("/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_student():
    response = client.get("/students/1")
    assert response.status_code == 200
    student = response.json()
    assert student["id"] == 1
    assert "name" in student

def test_get_student_not_found():
    response = client.get("/students/99")
    assert response.status_code == 404

def test_create_student():
    new_student_data = {"name": "Test Student", "age": 25, "email": "test@example.com"}
    response = client.post("/students", json=new_student_data)
    assert response.status_code == 200
    created_student = response.json()
    assert "id" in created_student
    assert created_student["name"] == new_student_data["name"]

    # Verify student was added
    response = client.get(f"/students/{created_student['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == new_student_data["name"]

def test_update_student():
    updated_data = {"name": "Updated Name", "age": 30, "email": "updated@example.com"}
    response = client.put("/students/1", json=updated_data)
    assert response.status_code == 200
    updated_student = response.json()
    assert updated_student["name"] == updated_data["name"]
    assert updated_student["age"] == updated_data["age"]
    assert updated_student["email"] == updated_data["email"]

def test_update_student_not_found():
    updated_data = {"name": "Updated Name", "age": 30, "email": "updated@example.com"}
    response = client.put("/students/99", json=updated_data)
    assert response.status_code == 404

def test_delete_student():
    # First create a student to delete
    new_student_data = {"name": "To Be Deleted", "age": 25, "email": "delete@example.com"}
    response = client.post("/students", json=new_student_data)
    assert response.status_code == 200
    created_student_id = response.json()["id"]

    # Delete the student
    response = client.delete(f"/students/{created_student_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Student deleted successfully"}

    # Verify the student is deleted
    response = client.get(f"/students/{created_student_id}")
    assert response.status_code == 404

def test_delete_student_not_found():
    response = client.delete("/students/99")
    assert response.status_code == 404
