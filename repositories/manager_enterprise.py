from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from models.manager_enterprise import ManagerEnterprise
from repositories.base import AssociativeRepository


class ManagerEnterpriseRepository(AssociativeRepository[ManagerEnterprise]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ManagerEnterprise)

    async def add_manager_to_enterprise(self, manager_id: int, enterprise_id: int) -> ManagerEnterprise:
        manager_enterprise = ManagerEnterprise(manager_id=manager_id, enterprise_id=enterprise_id)
        return await self.create(manager_enterprise)

    async def remove_manager_from_enterprise(self, manager_id: int, enterprise_id: int) -> None:
        manager_enterprise = await self.session.execute(
            select(self.model).where(self.model.manager_id == manager_id, self.model.enterprise_id == enterprise_id)
        )
        manager_enterprise_instance = manager_enterprise.scalar_one_or_none()
        if manager_enterprise_instance:
            await self.delete(manager_enterprise_instance)

    async def get_manager_enterprises(self, manager_id: int, limit: int = 20, offset: int = 0):
        query = select(self.model).where(self.model.manager_id == manager_id).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_manager_enterprise_vehicles(
        self, manager_id: int, enterprise_id: int, limit: int = 20, offset: int = 0
    ):
        query = (
            select(self.model)
            .where(self.model.manager_id == manager_id, self.model.enterprise_id == enterprise_id)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_manager_enterprise_drivers(
        self, manager_id: int, enterprise_id: int, limit: int = 20, offset: int = 0
    ):
        query = (
            select(self.model)
            .where(self.model.manager_id == manager_id, self.model.enterprise_id == enterprise_id)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())


async def get_manager_enterprise_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return ManagerEnterpriseRepository(session)
