import datetime
import enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

from .base import Base


class Permission(enum.Enum):
    read_only = "read_only"
    full_access = "full_access"


class User(Base):
    username: Mapped[str] = mapped_column(server_default='0', unique=True)
    permission: Mapped[Permission] = mapped_column(server_default=Permission.read_only.value, nullable=False)
    registered_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    hashed_password: Mapped[str] = mapped_column(server_default='0')
