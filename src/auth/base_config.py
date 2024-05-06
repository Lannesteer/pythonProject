from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend

from src import config
from src.auth.manager import get_user_manager
from src.auth.models import User

cookie_transport = CookieTransport(cookie_name='Clothing_store', cookie_max_age=3600)

SECRET = config.JWT_SECRET_KEY


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

