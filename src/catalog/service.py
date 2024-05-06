from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.base_class import BaseService
from src.catalog.models import Product
from src.database import get_async_session


class CatalogService(BaseService[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)

    async def get_list(self,
                       page: int = 1,
                       page_size: int = 10,
                       **kwargs
                       ):
        async with self.session as session:
            if not any(kwargs.values()):
                query = (
                    select(self.table)
                    .order_by(-self.table.id)
                )
            else:
                query = (
                    select(self.table)
                    .order_by(-self.table.id)
                )
                for key, value in kwargs.items():
                    if value is not None:
                        if key == "name":
                            query = query.filter(Product.name.ilike(f"%{value}%"))
                        elif key == "min_price":
                            query = query.filter(self.table.price >= value)
                        elif key == "max_price":
                            query = query.filter(self.table.price <= value)
                        else:
                            query = query.filter(getattr(self.table, key) == value)

            offset = (page - 1) * page_size
            query = query.offset(offset).limit(page_size)

            result = await session.execute(query)
            return result.scalars().all()


def get_catalog_service(session: AsyncSession = Depends(get_async_session)) -> CatalogService:
    return CatalogService(session)
