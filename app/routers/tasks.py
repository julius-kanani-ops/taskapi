from app.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

router = APIRouter()

@router.get("/", response_model=list[TaskResponse])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    
    query = select(Task)

    result = await db.execute(query)

    tasks = result.scalars().all()

    return tasks


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    
    new_task = Task(title=task.title)

    db.add(new_task)

    await db.commit()

    await db.refresh(new_task)

    return new_task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    # 1. Prepare the query to find exactly one task
    query = select(Task).where(Task.id == task_id)
    
    # 2. Execute the query
    result = await db.execute(query)
    
    # 3. Get the first result (or None if not found)
    task = result.scalar_one_or_none()
    
    # 4. Handle the "Not Found" case (The 404)
    if task is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Task with id {task_id} not found"
        )
        
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    # 1. Find the task first (to make sure it exists)
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    # 2. If it's not there, tell the user 404
    if task is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Task with id {task_id} not found"
        )

    # 3. Tell the session to delete the object
    await db.delete(task)
    
    # 4. Save the change to Postgres
    await db.commit()

    # 5. Return an empty response (standard for 204)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
