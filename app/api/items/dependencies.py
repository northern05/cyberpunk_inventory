from typing import Annotated

from fastapi import Path, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from app.core.models import db_helper
from app.core.models import Item
from app import exceptions


async def item_by_id(
        item_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Item:
    """
    Get Item by ID
    ---
    description: Retrieves details of a specific item by its ID.
    parameters:
        - name: item_id
          in: path
          description: ID of the item to retrieve
          required: true
          schema:
            type: integer
        - name: session
          in: query
          description: Database session object
          required: true
          schema:
            type: object
    responses:
        200:
            description: Returns the details of the item with the specified ID.
        404:
            description: Returns a 404 error if the item does not exist.
    """
    item = await crud.get_item(session=session, item_id=item_id)
    if item is not None:
        return item

    raise exceptions.ContentNotFound(
        detail=f"Item {item_id} not found!"
    )
