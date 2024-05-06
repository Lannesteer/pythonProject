from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.base_class import BaseService
from src.database import get_async_session
from src.support.models import Ticket
from src.support.schemas import TicketCreate, TicketAnswer


class SupportService(BaseService[Ticket]):
    def __init__(self, session: AsyncSession):
        super().__init__(Ticket, session)

    async def create(self,
                     data: TicketCreate,
                     user: User = Depends()
                     ):
        async with self.session as session:
            ticket = self.table(
                message=data.message,
                user_id=user.id
            )
            session.add(ticket)
            await session.commit()
        return ticket

    async def get_ticket(self,
                         ticket_id: int,
                         user: User = Depends()
                         ):
        async with self.session as session:
            if user.role_id == 1:
                query = (
                    select(self.table)
                    .filter_by(
                        id=ticket_id,
                        user_id=user.id
                    )
                )
            else:
                query = (
                    select(self.table)
                    .filter_by(id=ticket_id)
                )
            res = await session.execute(query)
            ticket = res.scalars().first()

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return ticket

    async def get_list(self,
                       page: int = 1,
                       page_size: int = 10,
                       user: User = Depends()
                       ):
        async with self.session as session:
            if user.role_id == 1:
                query = (
                    select(self.table)
                    .filter_by(user_id=user.id)
                    .order_by(-self.table.id)
                )
            else:
                query = (
                    select(self.table)
                    .order_by(-self.table.id.desc())
                )
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await session.execute(query)
        return result.scalars().all()


def get_support_service(session: AsyncSession = Depends(get_async_session)) -> SupportService:
    return SupportService(session)
