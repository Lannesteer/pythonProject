from datetime import datetime, timezone, timedelta

from jose import jwt
from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import UsersDAO
from src.auth.schemas import EmailModel
from src.auth.utils import verify_password
from src.database import get_async_session
from src import config


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, config.jwt_key.jwt, algorithm=config.jwt_key.algorithm)
    return encode_jwt


async def authenticate_user(email: EmailStr, password: str, session: AsyncSession = Depends(get_async_session)):
    user = await UsersDAO.find_one_or_none(session=session, filters=EmailModel(email=email))
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user
