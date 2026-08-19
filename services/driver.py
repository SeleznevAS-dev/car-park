from typing import Annotated

from fastapi import Depends

from repositories.driver import DriverRepository, get_driver_repository
from services.base import BaseService


class DriverService(BaseService[DriverRepository]):
    def __init__(self, repo: DriverRepository):
        super().__init__(repo)

    async def get_many(self, limit: int = 20, offset: int = 0) -> list:
        drivers = await self.repo.get_many(limit=limit, offset=offset)
        result = [
            {
                "id": driver.id,
                "name": driver.name,
                "surname": driver.surname,
                "salary": driver.salary,
                "enterprise_id": driver.enterprise_id,
                "driver_experience": driver.driver_experience,
                "created_at": driver.created_at,
                "updated_at": driver.updated_at,
                "vehicle_ids": [dv.vehicle_id for dv in driver.vehicles],
                "active_vehicle_id": await self.repo.get_active_vehicle_id(driver.id),
            }
            for driver in drivers
        ]
        return result


async def get_driver_service(repo: Annotated[DriverRepository, Depends(get_driver_repository)]):
    return DriverService(repo)
