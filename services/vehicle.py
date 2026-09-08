from typing import Annotated

from fastapi import Depends

from repositories.vehicle import VehicleRepository, get_vehicle_repository
from services.base import BaseService


class VehicleService(BaseService[VehicleRepository]):
    def __init__(self, repo: VehicleRepository):
        super().__init__(repo)

    async def get_by_enterprise_id(self, enterprise_id: int, limit: int = 20, offset: int = 0):
        return await self.repo.get_by_enterprise_id(enterprise_id=enterprise_id, limit=limit, offset=offset)


async def get_vehicle_service(repo: Annotated[VehicleRepository, Depends(get_vehicle_repository)]):
    return VehicleService(repo)
