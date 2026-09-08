from core.utils import to_dict_with_relation_ids
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
        result = result.scalars().all()
        return [to_dict_with_relation_ids(enterprise, "drivers") for enterprise in result]

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

    async def add_vehicle_to_enterprise(self, vehicle_id: int, enterprise_id: int):
        enterprise = await self.get_by_id(enterprise_id)
        if not enterprise:
            raise ValueError(f"Enterprise with id {enterprise_id} not found")

        vehicle = await self.session.get(Vehicle, vehicle_id)
        if not vehicle:
            raise ValueError(f"Vehicle with id {vehicle_id} not found")

        enterprise.vehicles.append(vehicle)
        await self.session.commit()
        return vehicle


async def get_enterprise_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return EnterpriseRepository(session)
