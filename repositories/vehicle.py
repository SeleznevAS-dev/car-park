from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from models.vehicle import Vehicle
from repositories.base import BaseRepository


class VehicleRepository(BaseRepository[Vehicle]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Vehicle)


async def get_vehicle_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return VehicleRepository(session)
