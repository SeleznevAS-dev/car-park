from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.database import get_session
from models.driver import Driver
from models.enterprise import Enterprise
from models.vehicle import Vehicle
from repositories.base import BaseRepository


class EnterpriseRepository(BaseRepository[Enterprise]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Enterprise)

    async def get_many(self, limit: int = 20, offset: int = 0) -> list[Enterprise]:
        query = (
            select(self.model)
            .options(
                selectinload(Enterprise.drivers).load_only(Driver.id),
                selectinload(Enterprise.vehicles).load_only(Vehicle.id),
            )
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_ids(self, ids: list[int]) -> list[Enterprise]:
        query = (
            select(self.model)
            .where(self.model.id.in_(ids))
            .options(
                selectinload(Enterprise.drivers).load_only(Driver.id),
                selectinload(Enterprise.vehicles).load_only(Vehicle.id),
            )
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())


async def get_enterprise_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return EnterpriseRepository(session)
