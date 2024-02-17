from typing import Annotated
from datetime import timedelta

from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper
from app.api.auth import helpers
from app.api.auth.schemas import UserCreate
from app.core.config import config

router_token = APIRouter(tags=["Users"])


@router_token.post("/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    """
    Login Endpoint
    ---
    description: Authenticate user and generate access token.
    responses:
        200:
            description: Successful login. Returns access token.
    """
    user = await helpers.authenticate_user(
        username=form_data.username,
        password=form_data.password,
        session=session
    )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = helpers.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router_token.post("/registration")
async def register(
        user_data: UserCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    """
    Registration Endpoint
    ---
    description: Register a new user.
    responses:
        200:
            description: Successful registration. Returns status "ok".
    """
    reg_user = await helpers.registrate_user(
        user_data=user_data,
        session=session
    )

    return {"ok": True}
