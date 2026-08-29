from pydantic import ConfigDict

from app.models.task import StatusEnum
from app.schemas.tag_pd import TagBase, TagRead
from app.schemas.task_pd import TaskBase
from app.schemas.user_pd import UserRead


class TaskRead(TaskBase):
    id: int
    status: StatusEnum
    tags: list[TagRead] | None = []
    user: UserRead | None = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserWithTasks(UserRead):
    tasks: list[TaskRead] = []

    model_config = ConfigDict(from_attributes=True)


class TagReadWithUsers(TagBase):
    users: list[UserRead] | None = []

    model_config = ConfigDict(from_attributes=True)
