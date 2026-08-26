from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.models.task import StatusEnum


class TagRead(BaseModel):
    name: str
    description: str
    amount: int

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: Optional[datetime] = None
    user_id: Optional[int] = None
    tags: List[int] = []


class TaskUpdate(TaskCreate):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: Optional[StatusEnum] = None
    user_id: Optional[int] = None
    tags: Optional[List[int]] = None


class TaskRead(BaseModel):
    title: str
    description: str
    deadline: Optional[datetime] = None
    status: StatusEnum
    tags: List[TagRead] = []
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
