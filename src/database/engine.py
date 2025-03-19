import settings

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine

url_object = URL.create(
    "postgresql+asyncpg",
    host="localhost",
    port=5432,
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    database=settings.POSTGRES_DB,
)

engine = create_async_engine(url_object)
