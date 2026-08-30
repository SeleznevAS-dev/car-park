from core.utils import to_dict_with_relation_ids
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from models.manager import Manager
from repositories.base import BaseRepository


class ManagerRepository(BaseRepository[Manager]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Manager)

    async def get_many(self, limit: int = 20, offset: int = 0):
        query = select(self.model).options(selectinload(Manager.enterprises)).limit(limit).offset(offset)
        result = await self.session.execute(query)
        managers = result.scalars().all()

        return [to_dict_with_relation_ids(manager, "enterprises") for manager in managers]


async def get_manager_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return ManagerRepository(session)
