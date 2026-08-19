from typing import Annotated

from fastapi import Depends

from repositories.brand import BrandRepository, get_brand_repository
from services.base import BaseService


class BrandService(BaseService):
    def __init__(self, repo: BrandRepository):
        super().__init__(repo)


async def get_brand_service(repo: Annotated[BrandRepository, Depends(get_brand_repository)]):
    return BrandService(repo)
