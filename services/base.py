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

    async def create(self, **kwargs):
        return await self.repo.create(**kwargs)

    async def update(self, id: int, **kwargs):
        model_instance = await self.repo.get_by_id(id)
        if not model_instance:
            return None
        for key, value in kwargs.items():
            setattr(model_instance, key, value)
        return await self.repo.update(model_instance)

    async def delete(self, model_instance):
        return await self.repo.delete(model_instance)

    async def delete_by_id(self, id: int):
        model_instance = await self.repo.get_by_id(id)
        if not model_instance:
            return None
        return await self.repo.delete(model_instance)


class AssociativeService(Generic[AssociativeRepoType], ABC):
    def __init__(self, repo: AssociativeRepoType):
        self.repo: AssociativeRepoType = repo

    async def get_many(self, limit: int = 20, offset: int = 0):
        return await self.repo.get_many(limit=limit, offset=offset)
