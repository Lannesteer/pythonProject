from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.auth.models import User
from src.base_class import BaseService
from src.database import get_async_session
from src.orders.schemas import OrderCreate, OrderItemCreate, OrderStatus, OrderCancel
from src.orders.models import Order, OrderItem


class OrderService(BaseService[Order]):
    def __init__(self, session: AsyncSession):
        super().__init__(Order, session)

    async def get_order(self,
                        order_id,
                        user: User
                        ):
        async with self.session as session:
            if user.role_id == 1:
                query = (
                    select(self.table)
                    .options(selectinload(self.table.items))
                    .filter_by(
                        id=order_id,
                        user_id=user.id
                    )
                )
            else:
                query = (
                    select(self.table)
                    .options(selectinload(self.table.items))
                    .filter_by(id=order_id)
                )

            res = await session.execute(query)
            order = res.scalars().first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        return order

    async def get_list(self,
                       page: int = 1,
                       page_size: int = 10,
                       user: User = Depends(),
                       ):
        async with self.session as session:
            if user.role_id == 1:
                query = (
                    select(self.table)
                    .options(selectinload(self.table.items))
                    .filter_by(user_id=user.id)
                    .order_by(-self.table.id.desc())
                )
            else:
                query = (
                    select(self.table)
                    .options(selectinload(self.table.items))
                    .order_by(-self.table.id.desc())
                )

            res = await session.execute(query)
            orders = res.scalars().all()
        return orders

    async def create_order(self,
                           order: OrderCreate,
                           order_items: List[OrderItemCreate],
                           user: User
                           ):
        async with self.session as session:
            new_order = self.table(
                user_id=user.id,
                total_amount=order.total_amount,
                status=OrderStatus.PENDING.value
            )
            session.add(new_order)
            await session.flush()

            for order_item in order_items:
                new_order_item = OrderItem(
                    product_id=order_item.product_id,
                    order_id=new_order.id,
                    quantity=order_item.quantity
                )
                session.add(new_order_item)

            await session.commit()

        return new_order

    async def cancel_order(self, order_id: int, user: User = Depends()):
        async with self.session as session:
            await self.get_order(order_id, user)

            await self.update(
                OrderCancel(status=OrderStatus.CANCELLED.value),
                order_id
            )

            await session.commit()
            return {'response': 'Your order has been cancelled'}


def get_order_service(session: AsyncSession = Depends(get_async_session)) -> OrderService:
    return OrderService(session)
