from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, BaseModel

from app.models.task import StatusEnum


class TaskBase(BaseModel):
    title: str
    description: str
    deadline: Optional[datetime] = None
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class TaskCreate(TaskBase):
    tag_ids: List[int] = []


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    tag_ids: Optional[List[int]] = None
