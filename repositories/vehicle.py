from sqlalchemy import select
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from models.vehicle import Vehicle
from repositories.base import BaseRepository


class VehicleRepository(BaseRepository[Vehicle]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Vehicle)

    async def get_by_enterprise_id(self, enterprise_id: int, limit: int = 20, offset: int = 0) -> list[Vehicle]:
        query = select(self.model).filter(self.model.enterprise_id == enterprise_id).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return list(result.scalars().all())


async def get_vehicle_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return VehicleRepository(session)
