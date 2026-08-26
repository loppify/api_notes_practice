from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.task_pd import TaskRead


class UserPydantic(BaseModel):
    username: str
    email: str
    password: str
    tasks: Optional[List[TaskRead]] = []

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
