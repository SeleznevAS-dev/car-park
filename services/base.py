from abc import ABC
from typing import Generic, TypeVar

from repositories.base import AssociativeRepository, BaseRepository

BaseRepoType = TypeVar("BaseRepoType", bound=BaseRepository)
AssociativeRepoType = TypeVar("AssociativeRepoType", bound=AssociativeRepository)


class BaseService(Generic[BaseRepoType], ABC):
    def __init__(self, repo: BaseRepoType):
        self.repo: BaseRepoType = repo

    async def get_many(self, limit: int = 20, offset: int = 0):
        return await self.repo.get_many(limit=limit, offset=offset)

    async def get_by_id(self, id: int):
        return await self.repo.get_by_id(id)


class AssociativeService(Generic[AssociativeRepoType], ABC):
    def __init__(self, repo: AssociativeRepoType):
        self.repo: AssociativeRepoType = repo

    async def get_many(self, limit: int = 20, offset: int = 0):
        return await self.repo.get_many(limit=limit, offset=offset)
