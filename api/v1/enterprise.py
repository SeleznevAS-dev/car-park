from models import User
from core.auth import fastapi_users
from fastapi import APIRouter, Depends

from services.enterprise import EnterpriseService, get_enterprise_service
from services.manager_enterprise import ManagerEnterpriseService, get_manager_enterprise_service

router = APIRouter()


@router.get("/")
async def get_enterprises(
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(fastapi_users.current_user()),
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
):
    if current_user.is_superuser:
        return await enterprise_service.get_many(limit=limit, offset=offset)

    manager_enterprises = await manager_enterprise_service.get_manager_enterprises(
        manager_id=current_user.id, limit=limit, offset=offset
    )
    if not manager_enterprises:
        return {"error": "No enterprises found for the current manager."}
    return await enterprise_service.get_by_ids([me.enterprise_id for me in manager_enterprises])


@router.get("/{id}")
async def get_enterprise(id: int, enterprise_service: EnterpriseService = Depends(get_enterprise_service)):
    enterprise = await enterprise_service.get_by_id(id)
    if not enterprise:
        return {"error": "Enterprise not found"}
    return enterprise


@router.post("/")
async def create_enterprise(
    name: str, city: str, enterprise_service: EnterpriseService = Depends(get_enterprise_service)
):
    return await enterprise_service.create(name=name, city=city)


@router.post("/{enterprise_id}/managers/{manager_id}")
async def add_manager_to_enterprise(
    enterprise_id: int,
    manager_id: int,
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
):
    return await manager_enterprise_service.add_manager_to_enterprise(
        manager_id=manager_id, enterprise_id=enterprise_id
    )


@router.delete("/{enterprise_id}/managers/{manager_id}")
async def remove_manager_from_enterprise(
    enterprise_id: int,
    manager_id: int,
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
):
    await manager_enterprise_service.remove_manager_from_enterprise(manager_id=manager_id, enterprise_id=enterprise_id)
    return {"message": "Manager removed from enterprise successfully."}


@router.get("/{enterprise_id}/managers")
async def get_enterprise_managers(
    enterprise_id: int,
    limit: int = 20,
    offset: int = 0,
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
):
    return await manager_enterprise_service.get_enterprise_managers(
        enterprise_id=enterprise_id, limit=limit, offset=offset
    )
