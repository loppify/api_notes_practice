from typing import Optional, List

from pydantic import ConfigDict

from app.models.task import StatusEnum
from app.schemas.tag_pd import TagRead, TagBase
from app.schemas.task_pd import TaskBase
from app.schemas.user_pd import UserBase


class TaskRead(TaskBase):
    id: int
    status: StatusEnum
    tags: Optional[List[TagRead]] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserRead(UserBase):
    id: int
    tasks: Optional[List[TaskRead]] = []

    model_config = ConfigDict(from_attributes=True)


class TagReadWithUsers(TagBase):
    id: int
    users: Optional[List[UserRead]] = []
