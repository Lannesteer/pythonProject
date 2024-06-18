from fastapi import FastAPI

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.sklad.router import router as sklad_operation
from src.orders.router import router as order_operation
from src.catalog.router import router as catalog_operation
from src.pages.router import router as pages
from src.support.router import router as support_chat

app = FastAPI(
    title="Clothes store"
)

# authentication

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(sklad_operation)
app.include_router(order_operation)
app.include_router(catalog_operation)
app.include_router(support_chat)
app.include_router(pages)



