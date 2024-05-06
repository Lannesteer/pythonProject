from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from src.auth.models import User
from src.auth.dependencies import get_current_admin_user
from src.catalog.schemas import ProductRead
from src.sklad.schemas import ProductCreateUpdate
from src.sklad.service import get_sklad_service, SkladService

router = APIRouter(
    prefix="/sklad",
    tags=["sklad_operation"]
)


@router.post(
    '/',
    response_model=ProductCreateUpdate,
    status_code=status.HTTP_201_CREATED
)
async def create_product(
        data: ProductCreateUpdate,
        user: User = Depends(get_current_admin_user),
        service: SkladService = Depends(get_sklad_service)
):
    return await service.create(data)


@router.post(
    '/parser',
    response_model=List[ProductCreateUpdate],
    status_code=status.HTTP_201_CREATED
)
async def add_products_from_parser(category_id: int,
                                   user: User = Depends(get_current_admin_user),
                                   service: SkladService = Depends(get_sklad_service)
                                   ):
    return await service.add_products_from_parser(category_id)


@router.get("/{product_id}/", response_model=ProductRead)
async def get_product(
        id_product: int,
        service: SkladService = Depends(get_sklad_service)
):
    return await service.get_one(id_product)


@router.patch("/{product_id}/", status_code=status.HTTP_200_OK)
async def update_product(
        product_id: int,
        data: ProductCreateUpdate,
        user: User = Depends(get_current_admin_user),
        service: SkladService = Depends(get_sklad_service)
):
    return await service.update(data, product_id)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_product(
        id_item: int,
        user: User = Depends(get_current_admin_user),
        service: SkladService = Depends(get_sklad_service)
):
    return await service.delete(id_item)
