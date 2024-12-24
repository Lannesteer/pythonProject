from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import authenticate_user, create_access_token
from src.auth.dependencies import UsersDAO, get_current_user, get_current_admin_user
from src.auth.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from src.auth.models import User
from src.auth.schemas import UserRegister, EmailModel, UserAddDB, UserAuth, UserInfo
from src.database import get_async_session

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register/")
async def register_user(user_data: UserRegister, session: AsyncSession = Depends(get_async_session)) -> dict:
    user = await UsersDAO.find_one_or_none(session=session, filters=EmailModel(email=user_data.email))
    if user:
        raise UserAlreadyExistsException
    user_data_dict = user_data.model_dump()
    del user_data_dict['confirm_password']
    await UsersDAO.add(session=session, values=UserAddDB(**user_data_dict))
    return {'message': f'Вы успешно зарегистрированы!'}


@router.post("/login/")
async def auth_user(response: Response, user_data: UserAuth, session: AsyncSession = Depends(get_async_session)):
    check = await authenticate_user(session=session, email=user_data.email, password=user_data.password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'message': 'Авторизация успешна!'}


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}


@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)) -> UserInfo:
    return UserInfo.model_validate(user_data)


@router.get("/all_users/")
async def get_all_users(session: AsyncSession = Depends(get_async_session),
                        user_data: User = Depends(get_current_admin_user)) -> List[UserInfo]:
    return await UsersDAO.find_all(session=session, filters=None)
