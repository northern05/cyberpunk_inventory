from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

from app.core.models import db_helper, Base
from app.api import router as router_v1
from app.core.config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(router=router_v1, prefix=config.api_v1_prefix)
add_pagination(app)
