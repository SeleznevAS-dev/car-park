from core.utils import to_dict_with_relation_ids
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.database import get_session
from models.driver import Driver
from models.driver_vehicle import DriverVehicle
from models.vehicle import Vehicle
from repositories.base import BaseRepository


class DriverRepository(BaseRepository[Driver]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Driver)

    async def get_many(self, limit: int = 20, offset: int = 0) -> list[Driver]:
        query = select(self.model).options(selectinload(Driver.vehicles)).limit(limit).offset(offset)
        result = await self.session.execute(query)
        drivers = result.scalars().all()

        result = [to_dict_with_relation_ids(driver, "vehicles") for driver in drivers]
        for driver in result:
            driver["active_vehicle_id"] = await self.get_active_vehicle_id(driver["id"])
        return result

    async def get_active_vehicle_id(self, driver_id: int) -> int:
        query = (
            select(Vehicle)
            .join(DriverVehicle, Vehicle.id == DriverVehicle.vehicle_id)
            .where(DriverVehicle.driver_id == driver_id and DriverVehicle.is_active)
        )
        result = await self.session.execute(query)
        vehicle = result.scalar_one_or_none()
        return vehicle.id if vehicle else -1

    async def get_drivers_by_enterprise_ids(self, enterprise_ids: list[int]) -> list[Driver]:
        query = (
            select(self.model)
            .where(self.model.enterprise_id.in_(enterprise_ids))
            .options(selectinload(Driver.vehicles))
        )
        result = await self.session.execute(query)
        drivers = result.scalars().all()

        result = [to_dict_with_relation_ids(driver, "vehicles") for driver in drivers]
        for driver in result:
            driver["active_vehicle_id"] = await self.get_active_vehicle_id(driver["id"])
        return result


async def get_driver_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return DriverRepository(session)
