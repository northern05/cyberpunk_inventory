from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page

from .schemas import ItemUpdate, ItemCreate
from app.core.models import Item


async def get_items(session: AsyncSession) -> Page[Item]:
    stmt = select(Item).order_by(Item.created_at.desc())
    result = await paginate(session, stmt)
    return result


async def get_item(session: AsyncSession, item_id: int) -> Item | None:
    return await session.get(Item, item_id)


async def create_item(session: AsyncSession, item_in: ItemCreate) -> Item:
    item = Item(**item_in.model_dump())
    session.add(item)
    await session.commit()
    return item


async def update_item(
        session: AsyncSession,
        item: Item,
        item_update: ItemUpdate,
        partial: bool = False,
) -> Item:
    for name, value in item_update.model_dump(exclude_unset=partial).items():
        if value is not None:
            setattr(item, name, value)
    await session.commit()
    return item


async def delete_item(
        session: AsyncSession,
        item: Item,
) -> None:
    await session.delete(item)
    await session.commit()
