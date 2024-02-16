from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page

from . import crud
from .dependencies import item_by_id
from .schemas import Item, ItemCreate, ItemUpdate
from app.core.models import db_helper

router = APIRouter(tags=["Items"])


@router.get("", response_model=Page[Item])
async def get_items(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_items(session=session)


@router.post(
    "",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
)
async def create_item(
        item_in: ItemCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_item(session=session, item_in=item_in)


@router.get("/{item_id}", response_model=Item)
async def get_item(
        item: Item = Depends(item_by_id),
):
    return item


@router.put("/{item_id}")
async def update_item(
        item_update: ItemUpdate,
        item: Item = Depends(item_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_item(
        session=session,
        item=item,
        item_update=item_update,
    )


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
        item: Item = Depends(item_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_item(session=session, item=item)
