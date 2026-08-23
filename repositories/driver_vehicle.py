from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from models.driver_vehicle import DriverVehicle
from repositories.base import AssociativeRepository


class DriverVehicleRepository(AssociativeRepository[DriverVehicle]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DriverVehicle)

    async def add_driver_to_vehicle(self, driver_id: int, vehicle_id: int) -> DriverVehicle:
        return await self.create(driver_id, vehicle_id)

    async def remove_driver_from_vehicle(self, driver_id: int, vehicle_id: int) -> None:
        driver_vehicle = await self.session.execute(
            select(self.model).where(self.model.driver_id == driver_id, self.model.vehicle_id == vehicle_id)
        )
        driver_vehicle_instance = driver_vehicle.scalar_one_or_none()
        if driver_vehicle_instance:
            await self.delete(driver_vehicle_instance)

    async def make_driver_active_for_vehicle(self, driver_id: int, vehicle_id: int) -> None:
        driver_vehicle = await self.session.execute(
            select(self.model).where(self.model.driver_id == driver_id, self.model.vehicle_id == vehicle_id)
        )
        driver_vehicle_instance = driver_vehicle.scalar_one_or_none()
        if driver_vehicle_instance:
            driver_vehicle_instance.is_active = True
            await self.session.commit()
            await self.session.refresh(driver_vehicle_instance)

    async def get_driver_vehicles(self, driver_id: int, limit: int = 20, offset: int = 0):
        query = select(self.model).where(self.model.driver_id == driver_id).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_vehicle_drivers(self, vehicle_id: int, limit: int = 20, offset: int = 0):
        query = select(self.model).where(self.model.vehicle_id == vehicle_id).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())


async def get_driver_vehicle_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return DriverVehicleRepository(session)
