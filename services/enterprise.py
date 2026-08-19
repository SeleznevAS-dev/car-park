from typing import Annotated

from fastapi import Depends

from repositories.enterprise import EnterpriseRepository, get_enterprise_repository
from services.base import BaseService


class EnterpriseService(BaseService[EnterpriseRepository]):
    def __init__(self, repo: EnterpriseRepository):
        super().__init__(repo)

    async def get_many(self, limit: int = 20, offset: int = 0) -> list:
        result = await self.repo.get_many(limit=limit, offset=offset)
        result = [
            {
                "id": enterprise.id,
                "name": enterprise.name,
                "created_at": enterprise.created_at,
                "updated_at": enterprise.updated_at,
                "driver_ids": [driver.id for driver in enterprise.drivers],
                "vehicle_ids": [vehicle.id for vehicle in enterprise.vehicles],
            }
            for enterprise in result
        ]
        return result

    async def get_by_ids(self, enterprise_ids: list[int]) -> list[dict]:
        enterprises = await self.repo.get_by_ids(enterprise_ids)
        return [
            {
                "id": enterprise.id,
                "name": enterprise.name,
                "created_at": enterprise.created_at,
                "updated_at": enterprise.updated_at,
                "driver_ids": [driver.id for driver in enterprise.drivers],
                "vehicle_ids": [vehicle.id for vehicle in enterprise.vehicles],
            }
            for enterprise in enterprises
        ]


async def get_enterprise_service(repo: Annotated[EnterpriseRepository, Depends(get_enterprise_repository)]):
    return EnterpriseService(repo)
