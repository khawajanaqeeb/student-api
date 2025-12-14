from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from models import Student, StudentCreate
from database import db_manager, get_session
from sqlmodel import Session, select

@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    db_manager.initialize_database()
    yield
    # on shutdown
    # (add cleanup code here if needed)

app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return {"message": "Hello, form FAST Api!"}

@app.get("/students", response_model=list[Student])
def get_students(session: Session = Depends(get_session)):
    students = session.execute(select(Student)).scalars().all()
    return students

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/students", response_model=Student)
def create_student(student: StudentCreate, session: Session = Depends(get_session)):
    db_student = Student.model_validate(student)
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.name = updated_student.name
    student.age = updated_student.age
    student.email = updated_student.email
    
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    session.delete(student)
    session.commit()
    return {"message": "Student deleted successfully"}