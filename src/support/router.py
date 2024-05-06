from typing import List

from fastapi import APIRouter, WebSocket, Depends, Query, status


from src.auth.dependencies import current_user, get_current_admin_user
from src.auth.models import User
from src.support.manager import websocket_handler
from src.support.service import get_support_service, SupportService
from src.support.schemas import TicketRead, TicketCreate, TicketAnswer

router = APIRouter(
    prefix="/support",
    tags=["support chat"]
)


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket_handler(websocket, client_id)


@router.patch("/", status_code=status.HTTP_200_OK)
async def create_ticket(ticket: TicketCreate,
                        user: User = Depends(current_user),
                        service: SupportService = Depends(get_support_service)
                        ):
    return await service.create(ticket, user)


@router.get("/{ticket_id}/", response_model=TicketRead)
async def get_ticket(ticket_id: int,
                     user: User = Depends(current_user),
                     service: SupportService = Depends(get_support_service)
                     ):
    return await service.get_ticket(ticket_id, user)


@router.get("/", response_model=List[TicketRead])
async def get_all_tickets(page: int = Query(1, gt=0),
                          page_size: int = Query(10, gt=0),
                          user: User = Depends(current_user),
                          service: SupportService = Depends(get_support_service)
                          ):
    return await service.get_list(page, page_size, user)


@router.patch("/{ticket_id}",
              status_code=status.HTTP_200_OK,
              response_description="You answered."
              )
async def answer_to_ticket(ticket_id: int,
                           data: TicketAnswer,
                           user: User = Depends(get_current_admin_user),
                           service: SupportService = Depends(get_support_service)
                           ):
    return await service.update(data, ticket_id)