from typing import Annotated
from fastapi import Path, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper, Item
from . import crud
from app.core.config import config


async def item_by_id(
        item_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Item:
    item = await crud.get_item(session=session, item_id=item_id)
    if item is not None:
        return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item {item_id} not found!",
    )


async def verify_token(req: Request):
    token = req.headers.get("Authorization")
    if token != config.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong API key"
        )
