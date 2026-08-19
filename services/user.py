from typing import Annotated

from fastapi import Depends

from repositories.user import UserRepository, get_user_repository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user_by_id(self, user_id: int):
        return await self.repo.get(user_id)

    async def get_user_by_email(self, email: str):
        return await self.repo.get_by_email(email)

    async def create_user(self, user):
        return await self.repo.create(user)

    async def update_user(self, user, update_dict: dict):
        return await self.repo.update(user, update_dict)

    async def delete_user(self, user):
        return await self.repo.delete(user)


async def get_user_service(repo: Annotated[UserRepository, Depends(get_user_repository)]):
    return UserService(repo)
