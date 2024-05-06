from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.catalog.models import Product
from src.database import Base
from src.orders.schemas import OrderStatus

if TYPE_CHECKING:
    from src.auth.models import User


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    total_amount: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    status: Mapped[OrderStatus]

    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")
    user: Mapped["User"] = relationship(back_populates='order')


class OrderItem(Base):
    __tablename__ = "order_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"), nullable=True)
    quantity: Mapped[int] = mapped_column(default=1)

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="order_item")
