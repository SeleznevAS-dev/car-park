from abc import ABC
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import AssociativeBase
from models.base import ModelBase as Base

BaseModelType = TypeVar("BaseModelType", bound=Base)
AssociativeModelType = TypeVar("AssociativeModelType", bound=AssociativeBase)


class BaseRepository(ABC, Generic[BaseModelType]):
    def __init__(self, session: AsyncSession, model: Type[BaseModelType]):
        self.session = session
        self.model = model

    async def get_by_id(self, id: int) -> Optional[BaseModelType]:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_many(self, limit: int = 20, offset: int = 0) -> List[BaseModelType]:
        query = select(self.model).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_all(self) -> List[BaseModelType]:
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, instance: BaseModelType) -> BaseModelType:
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: BaseModelType) -> BaseModelType:
        await self.session.merge(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: BaseModelType) -> None:
        await self.session.delete(instance)
        await self.session.commit()

    async def delete_by_id(self, id: int) -> bool:
        instance = await self.get_by_id(id)
        if instance:
            await self.delete(instance)
            return True
        return False


class AssociativeRepository(ABC, Generic[AssociativeModelType]):
    def __init__(self, session: AsyncSession, model: Type[AssociativeModelType]):
        self.session = session
        self.model = model

    async def get_many(self, limit: int = 20, offset: int = 0) -> List[AssociativeModelType]:
        query = select(self.model).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_all(self) -> List[AssociativeModelType]:
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, instance: AssociativeModelType) -> AssociativeModelType:
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: AssociativeModelType) -> None:
        await self.session.delete(instance)
        await self.session.commit()
