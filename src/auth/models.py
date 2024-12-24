from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base
from src.support.models import Ticket

if TYPE_CHECKING:
    from src.orders.models import Order


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    user: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    registration_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    phone_number: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), default=1, server_default=text("1"))

    order: Mapped["Order"] = relationship(back_populates="user")
    role: Mapped["Role"] = relationship("Role", back_populates="user", lazy="joined")
    tickets: Mapped["Ticket"] = relationship(back_populates="user")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
