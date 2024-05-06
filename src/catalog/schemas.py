from enum import Enum

from fastapi_users.schemas import PYDANTIC_V2
from pydantic import BaseModel, ConfigDict


class ProductRead(BaseModel):
    id: int
    name: str
    price: int
    quantity: int
    description: str
    season_id: int
    category_id: int
    subtype_id: int
    brands_id: int

    if PYDANTIC_V2:
        model_config = ConfigDict(from_attributes=True)
    else:
        class Config:
            orm_mode = True
