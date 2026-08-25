from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from app.models.task import StatusEnum

class TagBase(BaseModel):
    name: str
    description: str
    amount: int

    model_config = ConfigDict(from_attributes=True)

class TaskBase(BaseModel):
    title: str
    description: str
    deadline: datetime
    status: StatusEnum

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

class TaskTags(TaskBase):
    tags: List[TagBase] = []

class TasksByTag(TagBase):
    tasks: List[TaskTags] = []