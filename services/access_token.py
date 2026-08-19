from typing import Annotated

from fastapi import Depends

from repositories.access_token import AccessTokenRepository, get_access_token_repository
from fastapi_users.authentication.strategy import DatabaseStrategy
from core.config import settings


class AccessTokenService:
    def __init__(self, repo: AccessTokenRepository):
        self.repo = repo
        self.strategy = DatabaseStrategy(
            self.repo, lifetime_seconds=settings.access_token.TOKEN_LIFETIME_SECONDS
        )

    async def read_token(self, token: str | None, user_manager):
        return await self.strategy.read_token(token, user_manager)

    async def write_token(self, user):
        return await self.strategy.write_token(user)

    async def destroy_token(self, token: str, user):
        return await self.strategy.destroy_token(token, user)


async def get_access_token_service(repo: Annotated[AccessTokenRepository, Depends(get_access_token_repository)]):
    return AccessTokenService(repo)
