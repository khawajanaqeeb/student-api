from sqlmodel import Field, SQLModel

class StudentBase(SQLModel):
    name: str
    age: int
    email: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
