from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

app = FastAPI()

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None

class Task(TaskBase):
    id: int

_tasks: Dict[int, Task] = {}
_next_id = 1

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    global _next_id
    task_obj = Task(id=_next_id, **task.dict())
    _tasks[_next_id] = task_obj
    _next_id += 1
    return task_obj

@app.get("/tasks", response_model=List[Task])
def list_tasks():
    return list(_tasks.values())

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = _tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    existing = _tasks.get(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_update.dict(exclude_unset=True)
    updated = existing.copy(update=update_data)
    _tasks[task_id] = updated
    return updated

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del _tasks[task_id]
    return {"ok": True}
