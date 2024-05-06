from datetime import datetime
from enum import Enum
from typing import List

from fastapi_users.schemas import PYDANTIC_V2
from pydantic import BaseModel, ConfigDict


class OrderStatus(Enum):
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    total_amount: int


class OrderCancel(BaseModel):
    status: OrderStatus


class OrderItemRead(BaseModel):
    id: int
    product_id: int
    order_id: int
    quantity: int

    if PYDANTIC_V2:
        model_config = ConfigDict(from_attributes=True)
    else:
        class Config:
            orm_mode = True


class OrderRead(BaseModel):
    id: int
    user_id: int
    total_amount: int
    created_at: datetime
    status: str
    items: List[OrderItemRead]

    if PYDANTIC_V2:
        model_config = ConfigDict(from_attributes=True)
    else:
        class Config:
            orm_mode = True
