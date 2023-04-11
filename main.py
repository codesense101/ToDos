from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine ,Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound
from pydantic import BaseModel
from typing import List


## Initialize FastAPI
app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Database Configuration and connection
DATABASE_URL = "postgresql://postgres:password@localhost:5432/todoDB"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db: Session = SessionLocal()
Base: DeclarativeMeta = declarative_base()



## Create Tables
# define the Task model to match the schema of the tasks table
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)


## Pydantic Models
class TaskIn(BaseModel):
    title: str

class TaskStatusUpdate(BaseModel):
    completed: bool

class TaskOut(BaseModel):
    id: int
    title: str
    completed: bool
    class Config:
        orm_mode=True


## API Endpoints
@app.post("/api/tasks", response_model=TaskOut)
def create_task(task: TaskIn):
    db_task = Task(title=task.title)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# @app.get("/api/tasks")
@app.get("/api/tasks", response_model=List[TaskOut])
def read_tasks():
    tasks = db.query(Task).all()
    return tasks

@app.patch("/api/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskStatusUpdate):
    try:
        db_task = db.query(Task).filter(Task.id == task_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Task not found")
    print(task)
    print(task.completed)
    db_task.completed = task.completed
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        db_task = db.query(Task).filter(Task.id == task_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}

