import asyncio
from services.vehicle import VehicleService, get_vehicle_service
from services.driver import get_driver_service, DriverService
from services.enterprise import EnterpriseService, get_enterprise_service
from fastapi import APIRouter, Depends, HTTPException

from services.manager import ManagerService, get_manager_service
from services.manager_enterprise import ManagerEnterpriseService, get_manager_enterprise_service

router = APIRouter()


@router.get("/")
async def get_managers(
    limit: int = 20,
    offset: int = 0,
    manager_service: ManagerService = Depends(get_manager_service),
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
):
    managers = await manager_service.get_many(limit=limit, offset=offset)

    result = [
        {
            "id": manager.id,
            "created_at": manager.created_at,
            "updated_at": manager.updated_at,
            "enterprise_ids": [
                enterprise.enterprise_id
                for enterprise in await manager_enterprise_service.get_manager_enterprises(manager_id=manager.id)
            ],
        }
        for manager in managers
    ]
    return result


@router.get("/{id}")
async def get_manager(
    id: int,
    manager_service: ManagerService = Depends(get_manager_service),
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
):
    manager = await manager_service.get_by_id(id)
    manager_enterprises = await manager_enterprise_service.get_manager_enterprises(manager_id=manager.id)

    if not manager:
        return {"error": "Manager not found"}

    result = {
        "id": manager.id,
        "created_at": manager.created_at,
        "updated_at": manager.updated_at,
        "enterprise_ids": [enterprise.enterprise_id for enterprise in manager_enterprises],
    }
    return result


@router.post("/")
async def create_manager(user_id: int, manager_service: ManagerService = Depends(get_manager_service)):
    return await manager_service.create(user_id=user_id)


@router.get("/{manager_id}/enterprises")
async def get_manager_enterprises(
    manager_id: int,
    limit: int = 20,
    offset: int = 0,
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
):
    manager_enterprises = await manager_enterprise_service.get_manager_enterprises(
        manager_id=manager_id, limit=limit, offset=offset
    )
    if not manager_enterprises:
        raise HTTPException(status_code=404, detail="Manager not found or has no enterprises")

    result = enterprise_service.get_by_ids([me.enterprise_id for me in manager_enterprises])
    return await result
