from typing import Annotated

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page

from . import crud
from .dependencies import item_by_id
from .schemas import Item, ItemCreate, ItemUpdate, UserRead
from app.core.models import db_helper
from app.api.auth.helpers import get_current_user
from app import exceptions

router = APIRouter(tags=["Items"])


@router.get("", response_model=Page[Item], summary="Retrieve a list of items")
async def get_items(
        current_user: Annotated[UserRead, Depends(get_current_user)],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """
    Retrieve a list of items.

    - **Permissions:** Requires read-only or full access permission.
    """
    if current_user.permission.value not in ("read_only", "full_access"):
        raise exceptions.Unauthorized(detail="You don't have permissions!")
    return await crud.get_items(session=session)


@router.post(
    "",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item"
)
async def create_item(
        item_in: ItemCreate,
        current_user: Annotated[UserRead, Depends(get_current_user)],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """
    Create a new item.

    - **Permissions:** Requires full access permission.
    """
    if current_user.permission.value != "full_access":
        raise exceptions.Unauthorized(detail="You don't have permissions!")
    return await crud.create_item(session=session, item_in=item_in)


@router.get("/{item_id}", response_model=Item, summary="Retrieve details of a specific item by its ID")
async def get_item(
        current_user: Annotated[UserRead, Depends(get_current_user)],
        item: Item = Depends(item_by_id),
) -> Item:
    """
    Retrieve details of a specific item by its ID.

    - **Permissions:** Requires read-only or full access permission.
    """
    if current_user.permission.value not in ("read_only", "full_access"):
        raise exceptions.Unauthorized(detail="You don't have permissions!")
    return item


@router.put("/{item_id}", summary="Update details of a specific item by its ID")
async def update_item(
        current_user: Annotated[UserRead, Depends(get_current_user)],
        item_update: ItemUpdate,
        item: Item = Depends(item_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """
    Update details of a specific item by its ID.

    - **Permissions:** Requires full access permission.
    """
    if current_user.permission.value != "full_access":
        raise exceptions.Unauthorized(detail="You don't have permissions!")
    return await crud.update_item(
        session=session,
        item=item,
        item_update=item_update,
    )


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a specific item by its ID")
async def delete_item(
        current_user: Annotated[UserRead, Depends(get_current_user)],
        item: Item = Depends(item_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    """
    Delete a specific item by its ID.

    - **Permissions:** Requires full access permission.
    """
    if current_user.permission.value != "full_access":
        raise exceptions.Unauthorized(detail="You don't have permissions!")
    await crud.delete_item(session=session, item=item)
