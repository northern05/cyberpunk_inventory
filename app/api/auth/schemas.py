from typing import Optional

from pydantic import BaseModel

from app.core.models.user import Permission


class UserBase(BaseModel):
    username: str
    password: str
    permission: Optional[Permission] = Permission.read_only.value


class UserCreate(UserBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
