from typing import List

from fastapi import APIRouter, Depends, Query, status

from src.auth.models import User
from src.auth.dependencies import get_current_user
from src.orders.schemas import OrderCreate, OrderItemCreate, OrderRead
from src.orders.service import OrderService, get_order_service

router = APIRouter(
    prefix='/order',
    tags=['order_operation']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate,
                       order_item: List[OrderItemCreate],
                       user: User = Depends(get_current_user),
                       service: OrderService = Depends(get_order_service)
                       ):
    return await service.create_order(order, order_item, user)


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: int,
                    user: User = Depends(get_current_user),
                    service: OrderService = Depends(get_order_service)
                    ):
    return await service.get_order(order_id, user)


@router.get("/", response_model=List[OrderRead])
async def get_all_orders(page: int = Query(1, gt=0),
                         page_size: int = Query(10, gt=0),
                         user: User = Depends(get_current_user),
                         service: OrderService = Depends(get_order_service)
                         ):
    return await service.get_list(page, page_size, user)


@router.patch("/{order_id}", status_code=status.HTTP_200_OK)
async def cancel_order(order_id: int,
                       user: User = Depends(get_current_user),
                       service: OrderService = Depends(get_order_service)
                       ):
    return await service.cancel_order(order_id, user)
