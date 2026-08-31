from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class UserUpdate(UserBase):
    username: str | None
    email: str | None
    password: str | None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
