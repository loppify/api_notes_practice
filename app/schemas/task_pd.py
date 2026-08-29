from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.task import StatusEnum


class TaskBase(BaseModel):
    title: str
    description: str
    deadline: datetime | None = None
    user_id: int | None = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class TaskCreate(TaskBase):
    tag_ids: list[int] = []


class TaskUpdate(TaskBase):
    title: str | None = None
    description: str | None = None
    status: StatusEnum | None = None
    tag_ids: list[int] | None = None
    deadline: datetime | None = None
