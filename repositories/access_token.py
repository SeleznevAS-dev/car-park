from typing import Annotated

from fastapi import Depends
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from models.access_token import AccessToken


class AccessTokenRepository(SQLAlchemyAccessTokenDatabase[AccessToken]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AccessToken)


async def get_access_token_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return AccessTokenRepository(session)
