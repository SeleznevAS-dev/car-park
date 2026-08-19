from typing import Annotated

from fastapi import Depends

from repositories.vehicle import VehicleRepository, get_vehicle_repository
from services.base import BaseService


class VehicleService(BaseService):
    def __init__(self, repo: VehicleRepository):
        super().__init__(repo)


async def get_vehicle_service(repo: Annotated[VehicleRepository, Depends(get_vehicle_repository)]):
    return VehicleService(repo)
