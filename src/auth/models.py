from datetime import datetime
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base
from src.support.models import Ticket

if TYPE_CHECKING:
    from src.orders.models import Order


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="role")


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    registration_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    order: Mapped["Order"] = relationship(back_populates="user")
    role: Mapped["Role"] = relationship(back_populates="user")
    tickets: Mapped["Ticket"] = relationship(back_populates="user")
