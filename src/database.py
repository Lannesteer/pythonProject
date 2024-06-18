from typing import AsyncGenerator

from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import db_config, redis_config, RedisConfig, DbConfig


class Base(DeclarativeBase):
    pass


class AsyncDataBase:
    def __init__(self, db_config: DbConfig, redis_config: RedisConfig):
        self.database_url = f"postgresql+asyncpg://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.name}"
        self.redis = aioredis.from_url(f"redis://{redis_config.host}:{redis_config.port}")
        self.engine = create_async_engine(self.database_url)
        self.async_session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session


async_db = AsyncDataBase(db_config, redis_config)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in async_db.get_async_session():
        yield session
