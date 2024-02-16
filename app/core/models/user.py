import datetime
import enum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

from .base import Base


class Permission(enum.Enum):
    read_only = "read_only"
    full_access = "full_access"


class User(SQLAlchemyBaseUserTable[int], Base):
    username: Mapped[str] = mapped_column(server_default='0', unique=True)
    email: Mapped[str] = mapped_column(server_default='0')
    permission: Mapped[Permission] = mapped_column(server_default=Permission.read_only.value, nullable=False)

    registered_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    hashed_password: Mapped[str] = mapped_column(server_default='0')
    is_active: Mapped[bool] = mapped_column(server_default='false')
    is_superuser: Mapped[bool] = mapped_column(server_default='false')
    is_verified: Mapped[bool] = mapped_column(server_default='false')
