from typing import TypeVar, Generic, Type, Optional, Union

from fastapi import HTTPException
from sqlalchemy import select, update, delete

from sqlalchemy.ext.asyncio import AsyncSession


from src.database import Base

ModelType = TypeVar('ModelType', bound=Base)


class BaseService(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.table = model
        self.session = session

    async def get_list(self, limit: Optional[int] = None):
        async with self.session as session:
            query = await session.execute(
                select(self.table).limit(limit).order_by(-self.table.id.desc())
            )
            return query.scalars().all()

    async def get_one(self, item_id: Optional[Union[str, int]] = None):
        async with self.session as session:
            if isinstance(item_id, int):
                item = await session.execute(
                    select(self.table).filter_by(id=item_id)
                )
            elif isinstance(item_id, str):
                item = await session.execute(
                    select(self.table).filter_by(name=item_id)
                )
            db_item = item.scalar()

        if not db_item:
            raise HTTPException(status_code=404, detail="Page not found")
        return db_item

    async def create(self, data):
        async with self.session as session:
            item = self.table(**data.dict())
            session.add(item)
            await session.commit()
        return item

    async def update(self, data, item_id: int):
        async with self.session as session:
            await session.execute(update(self.table).filter_by(id=item_id), data.dict())
            await session.commit()
        return await self.get_one(item_id)

    async def delete(self, id_item):
        async with self.session as session:
            await session.execute(delete(self.table).filter_by(id=id_item))
            await session.commit()
        return {'response': 'deleted'}



