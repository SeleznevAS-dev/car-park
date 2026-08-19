from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from models.manager import Manager
from repositories.base import BaseRepository


class ManagerRepository(BaseRepository[Manager]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Manager)


async def get_manager_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return ManagerRepository(session)
