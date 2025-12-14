from fastapi import FastAPI, HTTPException
from sqlmodel import Field, SQLModel # Removed BaseModel import

app = FastAPI()

class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
    email: str

# Demo students - now storing Student (SQLModel) objects
students: list[Student] = [
    Student(id=1, name="Fatima Zahra", age=20, email="fatima.zahra@example.com"),
    Student(id=2, name="Ali Hassan", age=22, email="ali.hassan@example.com"),
    Student(id=3, name="Ayesha Khan", age=21, email="ayesha.khan@example.com"),
]

@app.get("/")
def home():
    return {"message": "Hello, form FAST Api!"}

@app.get("/students")
def get_students():
    return students

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    for student in students:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

@app.post("/students", response_model=Student)
def create_student(student: Student):
    new_id = max(s.id for s in students) + 1 if students else 1
    student.id = new_id
    students.append(student)
    return student

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student):
    for i, student in enumerate(students):
        if student.id == student_id:
            student.name = updated_student.name
            student.age = updated_student.age
            student.email = updated_student.email
            return student
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    global students
    original_len = len(students)
    students = [student for student in students if student.id != student_id]
    if len(students) == original_len:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}