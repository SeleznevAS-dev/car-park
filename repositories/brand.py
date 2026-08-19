from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from models.brand import Brand
from repositories.base import BaseRepository


class BrandRepository(BaseRepository[Brand]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Brand)


async def get_brand_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return BrandRepository(session)
