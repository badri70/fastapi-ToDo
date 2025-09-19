from datetime import date
from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    complete: bool = False
    user_id: int


class TaskUpdate(TaskBase):
    title: str | None = None
    description: str | None = None
    complete: bool | None = None


class TaskInDBBase(TaskBase):
    id: int
    complete: bool
    created_at: date

    class Config:
        from_attributes = True