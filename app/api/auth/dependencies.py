from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from app.core.models import db_helper


async def get_user_db(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    yield SQLAlchemyUserDatabase(session, User)
