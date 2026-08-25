from typing import List

from pydantic import BaseModel, ConfigDict

from app.schemas.task_pd import TaskBase


class UserPydantic(BaseModel):
    username: str
    email: str
    password: str
    tasks: List[TaskBase]

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
