from datetime import datetime, timezone

import jwt
from fastapi import Depends, status, HTTPException
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import TokenNoFound, NoJwtException, TokenExpiredException, NoUserIdException
from src import config
from src.auth.manager import BaseDAO
from src.database import get_async_session
from src.auth.models import User, Role
from fastapi import Request


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise TokenNoFound
    return token


async def get_current_user(token: str = Depends(get_token), session: AsyncSession = Depends(get_async_session)):
    try:
        payload = jwt.decode(token, config.jwt_key.jwt, algorithms=config.jwt_key.algorithm)
    except JWTError:
        raise NoJwtException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await UsersDAO.find_one_or_none_by_id(data_id=int(user_id), session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user


async def get_current_admin_user(user: User = Depends(get_current_user)):
    if user.role_id != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to perform this action",
        )
    return user


class UsersDAO(BaseDAO):
    model = User


class RoleDAO(BaseDAO):
    model = Role
