from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    email: str

# Demo students
students = [
    {"id": 1, "name": "Fatima Zahra", "age": 20, "email": "fatima.zahra@example.com"},
    {"id": 2, "name": "Ali Hassan", "age": 22, "email": "ali.hassan@example.com"},
    {"id": 3, "name": "Ayesha Khan", "age": 21, "email": "ayesha.khan@example.com"},
]

@app.get("/")
def home():
    return {"message": "Hello, form FAST Api!"}

@app.get("/students")
def get_students():
    return students

@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

@app.post("/students")
def create_student(student: Student):
    new_id = max(s["id"] for s in students) + 1 if students else 1
    new_student = {"id": new_id, **student.model_dump()}
    students.append(new_student)
    return new_student

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    for i, student in enumerate(students):
        if student["id"] == student_id:
            students[i] = {"id": student_id, **updated_student.model_dump()}
            return students[i]
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    global students
    original_len = len(students)
    students = [student for student in students if student["id"] != student_id]
    if len(students) == original_len:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}