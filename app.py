from fastapi import FastAPI

from src.sklad.router import router as sklad_operation
from src.orders.router import router as order_operation
from src.catalog.router import router as catalog_operation
from src.pages.router import router as pages
from src.support.router import router as support_chat
from src.auth.router import router as auth_router

app = FastAPI(
    title="Clothes store"
)

app.include_router(auth_router)
app.include_router(sklad_operation)
app.include_router(order_operation)
app.include_router(catalog_operation)
app.include_router(support_chat)
app.include_router(pages)



