from typing import Annotated

from fastapi import Depends

from repositories.driver import DriverRepository, get_driver_repository
from services.base import BaseService


class DriverService(BaseService[DriverRepository]):
    def __init__(self, repo: DriverRepository):
        super().__init__(repo)

    async def get_many(self, limit: int = 20, offset: int = 0) -> list:
        drivers = await self.repo.get_many(limit=limit, offset=offset)
        return drivers

    async def get_drivers_by_enterprise_ids(self, enterprise_ids: list[int]) -> list:
        drivers = await self.repo.get_drivers_by_enterprise_ids(enterprise_ids=enterprise_ids)
        return drivers


async def get_driver_service(repo: Annotated[DriverRepository, Depends(get_driver_repository)]):
    return DriverService(repo)
