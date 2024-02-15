import os
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    DB_NAME: str = os.environ.get('DB_NAME', 'cyberpunk_inventory')
    DB_USER: str = os.environ.get('DB_USER', 'johnny_silverhand')
    DB_HOST: str = os.environ.get('DB_HOST', 'localhost')
    DB_PORT: str = os.environ.get('DB_PORT', '5432')
    DB_PW: str = os.environ.get('DB_PW', 'samurai')

    SQLALCHEMY_DATABASE_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    db_echo: bool = True
    API_KEY: str = os.environ.get('API_KEY', '0c95c7ece1ce1a9750275ef1c6d7ad6b278f70d66592207783ffe7d58474cc01')

config = Config()
