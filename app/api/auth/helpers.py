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
    """
    Get Current User
    ---
    description: Retrieve the current user based on the provided JWT token.
    parameters:
        - name: token
          in: header
          description: JWT token for authentication
          required: true
          schema:
            type: string
    responses:
        200:
            description: Successful retrieval. Returns the current user.
        401:
            description: Unauthorized access. Invalid or missing token.
        404:
            description: User not found.
    """
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
    """
    Register User
    ---
    description: Register a new user.
    parameters:
        - name: user_data
          in: body
          description: User data for registration
          required: true
          schema:
            $ref: '#/definitions/UserCreate'
    responses:
        200:
            description: Successful registration. Returns the registered user.
        400:
            description: Bad request. User already exists.
    """
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
    """
    Authenticate User
    ---
    description: Authenticate user with provided username and password.
    parameters:
        - name: username
          in: body
          description: Username for authentication
          required: true
          schema:
            type: string
        - name: password
          in: body
          description: Password for authentication
          required: true
          schema:
            type: string
    responses:
        200:
            description: Successful authentication. Returns the authenticated user.
        400:
            description: Bad request. Incorrect username or password.
    """
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
    """
    Get User
    ---
    description: Retrieve a user by username.
    parameters:
        - name: username
          in: body
          description: Username of the user to retrieve
          required: true
          schema:
            type: string
    responses:
        200:
            description: Successful retrieval. Returns the user.
    """
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalars().first()


def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
):
    """
    Create Access Token
    ---
    description: Generate an access token with optional expiration time.
    parameters:
        - name: data
          in: body
          description: Data to encode into the token
          required: true
          schema:
            type: object
        - name: expires_delta
          in: body
          description: Expiration time for the token (optional)
          schema:
            type: string
    responses:
        200:
            description: Successful token creation. Returns the access token.
    """
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
    """
    Verify Password
    ---
    description: Verify if the provided plain password matches the hashed password.
    parameters:
        - name: plain_password
          in: body
          description: Plain password to verify
          required: true
          schema:
            type: string
        - name: hashed_password
          in: body
          description: Hashed password to compare against
          required: true
          schema:
            type: string
    responses:
        200:
            description: Passwords match. Verification successful.
        400:
            description: Passwords do not match. Verification failed.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """
    Get Password Hash
    ---
    description: Generate a hash for the provided password.
    parameters:
        - name: password
          in: body
          description: Password to hash
          required: true
          schema:
            type: string
    responses:
        200:
            description: Successful hash generation. Returns the hashed password.
    """
    return pwd_context.hash(password)
