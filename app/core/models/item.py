import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
import enum

from .base import Base


class ItemCategory(enum.Enum):
    Weapon = "Weapon"
    Cybernetic = "Cybernetic"
    Gadget = "Gadget"

class Item(Base):

    name: Mapped[str] = mapped_column(server_default='0', unique=True)
    description: Mapped[str] = mapped_column(server_default='0')
    category: Mapped[ItemCategory] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(server_default='0')
    price: Mapped[float] = mapped_column(server_default='0')
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    def to_dict(self):
        return {
            "id": Base.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "quantity": self.quantity,
            "price": self.price,
            "created_at": self.created_at
        }