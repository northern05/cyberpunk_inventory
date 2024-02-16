from typing import Optional

from fastapi_users import schemas

from app.core.models.user import Permission


class UserRead(schemas.BaseUser):
    email: str
    username: str
    permission: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    permission: Optional[Permission]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    class Config:
        orm_mode = True

