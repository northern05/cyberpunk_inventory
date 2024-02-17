from datetime import datetime, timedelta, timezone
from typing import Annotated

from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from app.core.models import db_helper, User
from .schemas import UserCreate, TokenData
from app import exceptions
from app.core.config import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise exceptions.Unauthorized()
        token_data = TokenData(username=username)
    except JWTError:
        raise exceptions.Unauthorized()
    stmt = select(User).where(User.username == token_data.username)
    res = await session.execute(stmt)
    user = res.scalars().first()
    if not user:
        raise exceptions.ContentNotFound("User not exists!")
    return user


async def registrate_user(
        user_data: UserCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user = await get_user(username=user_data.username, session=session)
    if user:
        raise exceptions.UserAlreadyExists()
    hashed_password = pwd_context.hash(user_data.password)
    user = User(
        username=user_data.username,
        hashed_password=hashed_password,
        permission=user_data.permission,
        registered_at=datetime.now()
    )
    session.add(user)
    await session.commit()
    return user


async def authenticate_user(
        username: str,
        password: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user = await get_user(username=username, session=session)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    verification_result = verify_password(password, user.hashed_password)
    if not verification_result:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user


async def get_user(
        username: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalars().first()


def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def verify_password(
        plain_password: str,
        hashed_password: str
):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
