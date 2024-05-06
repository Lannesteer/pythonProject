from fastapi import Depends, status, HTTPException

from src.auth.base_config import fastapi_users
from src.auth.models import User

current_user = fastapi_users.current_user()


async def get_current_admin_user(user: User = Depends(current_user)):
    if user.role_id != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to perform this action",
        )
    return user
