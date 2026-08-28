from typing import Optional

from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class TagCreate(TagBase):
    user_id: Optional[int] = None


class TagRead(TagBase):
    id: int
    amount: int = 0
