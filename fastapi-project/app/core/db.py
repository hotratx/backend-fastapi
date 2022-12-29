from sys import modules
from typing import Optional
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from app.heroes.models import Hero

from app import settings
from sqlmodel import SQLModel, Field

# db_connection_str = settings.db_async_connection_str
if settings.tests:
    print("PYTEST")
    POSTGRES_URL = settings.db_async_test_connection_str
else:
    print("NO PYTEST")
    POSTGRES_URL = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_hostname}:{settings.database_port}/{settings.postgres_db}"


async_engine = create_async_engine(
    POSTGRES_URL,
    echo=True,
    future=True
)


async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


async def init_db():
    async with async_engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
