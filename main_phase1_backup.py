from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    id: int
    title: str
    completed: bool


class TaskCreate(BaseModel):
    title: str

class HealthCheck(BaseModel):
    status: str
    time: str

class Message(BaseModel):
    message: str

app = FastAPI()

tasks = [
    {"id": 1, "title": "Eat today at six.", "completed": True},
    {"id": 2, "title": "Sleep at 10 p.m.", "completed": False},
    {"id": 3, "title": "Wake up in the morning", "completed": False},
    {"id": 4, "title": "Buy milk", "completed": False, "user_password": "abc123"}
]

@app.get("/", response_model=HealthCheck)
async def index():
   return {"status": "ok", "time": datetime.now().isoformat()}


@app.get("/tasks", response_model=list[Task])
async def get_tasks():
    return tasks

@app.post("/tasks", status_code=201, response_model=Task)
async def create_task(task: TaskCreate):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "completed": False
    }

    tasks.append(new_task)
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task with task id: {task_id} not found")

@app.delete("/tasks/{task_id}", response_model=Message)
async def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully."}
    raise HTTPException(status_code=404, detail=f"Task with task id: {task_id} not found")
