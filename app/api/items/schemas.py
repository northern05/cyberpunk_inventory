from pydantic import BaseModel, ConfigDict
import datetime
from typing import Optional
from app.core.models.item import ItemCategory

class ItemBase(BaseModel):
    name: str
    description: str
    category: ItemCategory
    quantity: int
    price: float


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ItemCategory] = None
    quantity: Optional[int] = None
    price: Optional[float] = None


class Item(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    category: ItemCategory
    quantity: int
    price: float
    created_at: datetime.datetime
