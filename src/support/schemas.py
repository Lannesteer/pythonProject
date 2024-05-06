from datetime import datetime
from typing import Optional

from fastapi_users.schemas import PYDANTIC_V2
from pydantic import BaseModel, ConfigDict


class TicketCreate(BaseModel):
    message: str


class TicketAnswer(BaseModel):
    answer: str


class TicketRead(BaseModel):
    id: int
    message: str
    user_id: int
    date: datetime
    answer: Optional[str] = None

    if PYDANTIC_V2:
        model_config = ConfigDict(from_attributes=True)
    else:
        class Config:
            orm_mode = True
