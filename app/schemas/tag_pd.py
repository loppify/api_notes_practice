from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class TagCreate(TagBase):
    user_id: int | None = None


class TagRead(TagBase):
    id: int
    user_id: int | None = None


class TagReadWithAmount(TagRead):
    amount: int | None = None


class TagUpdate(TagBase):
    name: str | None = None
    description: str | None = None
