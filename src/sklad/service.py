import json
import random

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from parser.mappings import category_mapping, subtype_mapping, brand_mapping, filename_mapping
from src.sklad.schemas import ProductCreateUpdate
from src.base_class import BaseService
from src.catalog.models import Product
from src.database import get_async_session


class SkladService(BaseService[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)

    async def add_products_from_parser(self, category_id):
        with open(f'parser/data/{filename_mapping[category_id]}.json', 'r', encoding='UTF-8') as f:
            data = json.load(f)

        added_products = []

        for item in data.get('digitalData', {}).get('listing', {}).get('items', []):
            try:
                await self.get_one(item.get('name'))
            except HTTPException:
                brand = brand_mapping.get(item.get('manufacturer'))
                if brand is not None:
                    name = item.get('name'.strip())
                    category_id = category_mapping[item.get('category', [''])[1]]
                    subtype_id = subtype_mapping[item.get('lowestCategory')]
                    quantity = random.randint(10, 20)
                    price = item.get('unitPrice')
                    season_id = random.randint(1, 7)
                    brands_id = brand_mapping[item.get('manufacturer')]

                    product = ProductCreateUpdate(name=name,
                                                  category_id=category_id,
                                                  subtype_id=subtype_id,
                                                  quantity=quantity,
                                                  price=price,
                                                  season_id=season_id,
                                                  brands_id=brands_id
                                                  )
                    added_products.append(product)

                    await self.create(product)
        return added_products


def get_sklad_service(session: AsyncSession = Depends(get_async_session)) -> SkladService:
    return SkladService(session)
