from typing import List

from fastapi import APIRouter, Depends, Query

from src.catalog.service import CatalogService, get_catalog_service
from src.catalog.schemas import ProductRead

router = APIRouter(
    prefix="/catalog",
    tags=["product_operation"]
)


@router.get("/", response_model=List[ProductRead])
async def filter_products(page: int = Query(1, gt=0),
                          page_size: int = Query(10, gt=0),
                          category_id: int = None,
                          subtype_id: int = None,
                          season_id: int = None,
                          brands_id: int = None,
                          name: str = None,
                          min_price: float = None,
                          max_price: float = None,
                          service: CatalogService = Depends(get_catalog_service)
                          ):

    return await service.get_list(page=page, page_size=page_size,
                                  category_id=category_id,
                                  subtype_id=subtype_id,
                                  season_id=season_id,
                                  brands_id=brands_id,
                                  name=name,
                                  min_price=min_price,
                                  max_price=max_price
                                  )
