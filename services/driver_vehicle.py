from typing import Annotated

from fastapi import Depends

from repositories.driver_vehicle import DriverVehicleRepository, get_driver_vehicle_repository
from services.base import AssociativeService


class DriverVehicleService(AssociativeService[DriverVehicleRepository]):
    def __init__(self, repo: DriverVehicleRepository):
        super().__init__(repo)

    async def get_driver_vehicles(self, driver_id: int, limit: int = 20, offset: int = 0):
        return await self.repo.get_driver_vehicles(driver_id=driver_id, limit=limit, offset=offset)

    async def get_vehicle_drivers(self, vehicle_id: int, limit: int = 20, offset: int = 0):
        return await self.repo.get_vehicle_drivers(vehicle_id=vehicle_id, limit=limit, offset=offset)


async def get_driver_vehicle_service(repo: Annotated[DriverVehicleRepository, Depends(get_driver_vehicle_repository)]):
    return DriverVehicleService(repo)
