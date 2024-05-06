from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]


class Category(Base):
    __tablename__ = "category"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)

    product: Mapped["Product"] = relationship(back_populates="category")


class Brand(Base):
    __tablename__ = "brand"
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)

    product: Mapped["Product"] = relationship(back_populates="brand")


class Subtype(Base):
    __tablename__ = "subtype"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))

    product: Mapped["Product"] = relationship(back_populates="subtype")


class Season(Base):
    __tablename__ = "season"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)

    product: Mapped["Product"] = relationship(back_populates='seasons')


class Product(Base):
    __tablename__ = "product"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    season_id: Mapped[int] = mapped_column(ForeignKey('season.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    subtype_id: Mapped[int] = mapped_column(ForeignKey("subtype.id"))
    brands_id: Mapped[int] = mapped_column(ForeignKey("brand.id"))

    order_item: Mapped[list["OrderItem"]] = relationship(back_populates="product")
    category: Mapped["Category"] = relationship(back_populates="product")
    brand: Mapped["Brand"] = relationship(back_populates="product")
    subtype: Mapped["Subtype"] = relationship(back_populates="product")
    seasons: Mapped["Season"] = relationship(back_populates='product')

    def __str__(self) -> str:
        return self.name
