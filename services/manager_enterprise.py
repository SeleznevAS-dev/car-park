from typing import Annotated

from fastapi import Depends

from repositories.manager_enterprise import ManagerEnterpriseRepository, get_manager_enterprise_repository
from services.base import AssociativeService


class ManagerEnterpriseService(AssociativeService[ManagerEnterpriseRepository]):
    def __init__(self, repo: ManagerEnterpriseRepository):
        super().__init__(repo)

    async def get_enterprise_managers(self, enterprise_id: int, limit: int = 20, offset: int = 0):
        return await self.repo.get_enterprise_managers(enterprise_id=enterprise_id, limit=limit, offset=offset)

    async def get_manager_enterprises(self, manager_id: int, limit: int = 20, offset: int = 0):
        return await self.repo.get_manager_enterprises(manager_id=manager_id, limit=limit, offset=offset)

    async def add_manager_to_enterprise(self, manager_id: int, enterprise_id: int):
        return await self.repo.add_manager_to_enterprise(manager_id=manager_id, enterprise_id=enterprise_id)

    async def remove_manager_from_enterprise(self, manager_id: int, enterprise_id: int):
        return await self.repo.remove_manager_from_enterprise(manager_id=manager_id, enterprise_id=enterprise_id)

    async def get_manager_enterprise(self, manager_id: int, enterprise_id: int):
        return await self.repo.get_by_ids(manager_id=manager_id, enterprise_id=enterprise_id)


async def get_manager_enterprise_service(
    repo: Annotated[ManagerEnterpriseRepository, Depends(get_manager_enterprise_repository)],
):
    return ManagerEnterpriseService(repo)
