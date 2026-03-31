from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class TaskBase(BaseModel):
    title: str


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: str | None = None
    completed: bool | None = None


class TaskResponse(TaskBase):
    id: UUID
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

