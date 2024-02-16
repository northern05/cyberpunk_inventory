import os
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    DB_NAME: str = os.environ.get('DB_NAME')
    DB_USER: str = os.environ.get('DB_USER')
    DB_HOST: str = os.environ.get('DB_HOST')
    DB_PORT: str = os.environ.get('DB_PORT')
    DB_PW: str = os.environ.get('DB_PW')

    SQLALCHEMY_DATABASE_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    db_echo: bool = True

    SECRET_AUTH: str = os.environ.get('SECRET_AUTH')

config = Config()
