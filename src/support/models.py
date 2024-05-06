from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.auth.models import User


class Ticket(Base):
    __tablename__ = "ticket"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    answer: Mapped[str] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="tickets")


class ChatMessage(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str]
    date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

