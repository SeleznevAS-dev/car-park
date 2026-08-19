from typing import Annotated

from fastapi import Depends

from repositories.manager import ManagerRepository, get_manager_repository
from services.base import BaseService


class ManagerService(BaseService[ManagerRepository]):
    def __init__(self, repo: ManagerRepository):
        super().__init__(repo)


async def get_manager_service(repo: Annotated[ManagerRepository, Depends(get_manager_repository)]):
    return ManagerService(repo)
