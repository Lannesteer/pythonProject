from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield session
