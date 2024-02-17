from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page

from .schemas import ItemUpdate, ItemCreate
from app.core.models import Item


async def get_items(session: AsyncSession) -> Page[Item]:
    """
    Get Items
    ---
    description: Retrieves a paginated list of items ordered by creation date.
    parameters:
        - name: session
          in: body
          description: AsyncSession object for database access
          required: true
          schema:
            type: object
    responses:
        200:
            description: Returns a paginated list of items.
    """
    stmt = select(Item).order_by(Item.created_at.desc())
    result = await paginate(session, stmt)
    return result


async def get_item(session: AsyncSession, item_id: int) -> Item | None:
    """
    Get Item by ID
    ---
    description: Retrieves the item with the specified ID.
    parameters:
        - name: session
          in: body
          description: AsyncSession object for database access
          required: true
          schema:
            type: object
        - name: item_id
          in: path
          description: ID of the item to retrieve
          required: true
          schema:
            type: integer
    responses:
        200:
            description: Returns the item with the specified ID.
        404:
            description: Item not found.
    """
    return await session.get(Item, item_id)


async def create_item(session: AsyncSession, item_in: ItemCreate) -> Item:
    """
    Create Item
    ---
    description: Creates a new item with the provided data.
    parameters:
        - name: session
          in: body
          description: AsyncSession object for database access
          required: true
          schema:
            type: object
        - name: item_in
          in: body
          description: Data for creating the new item
          required: true
          schema:
            $ref: '#/components/schemas/ItemCreate'
    responses:
        200:
            description: Returns the newly created item.
    """
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
    """
    Update Item
    ---
    description: Updates the details of the specified item.
    parameters:
        - name: session
          in: body
          description: AsyncSession object for database access
          required: true
          schema:
            type: object
        - name: item
          in: body
          description: Item to be updated
          required: true
          schema:
            $ref: '#/components/schemas/Item'
        - name: item_update
          in: body
          description: Data for updating the item
          required: true
          schema:
            $ref: '#/components/schemas/ItemUpdate'
        - name: partial
          in: query
          description: Boolean flag indicating partial update
          required: false
          schema:
            type: boolean
    responses:
        200:
            description: Returns the updated item.
    """
    for name, value in item_update.model_dump(exclude_unset=partial).items():
        if value is not None:
            setattr(item, name, value)
    await session.commit()
    return item


async def delete_item(
        session: AsyncSession,
        item: Item,
) -> None:
    """
    Delete Item
    ---
    description: Deletes the specified item.
    parameters:
        - name: session
          in: body
          description: AsyncSession object for database access
          required: true
          schema:
            type: object
        - name: item
          in: body
          description: Item to be deleted
          required: true
          schema:
            $ref: '#/components/schemas/Item'
    responses:
        204:
            description: No content.
    """
    await session.delete(item)
    await session.commit()
