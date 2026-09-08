from schemas.enterprise import EnterpriseUpdateSchema
from models import User
from core.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Response, status

from services.enterprise import EnterpriseService, get_enterprise_service
from services.manager_enterprise import ManagerEnterpriseService, get_manager_enterprise_service

router = APIRouter()


@router.get("/")
async def get_enterprises(
    current_user: User = Depends(get_current_user),
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
):
    manager_enterprises = await manager_enterprise_service.get_manager_enterprises(manager_id=current_user.id)
    if not manager_enterprises:
        raise HTTPException(status_code=404, detail="Manager not found or has no enterprises")

    return await enterprise_service.get_by_ids([me.enterprise_id for me in manager_enterprises])


@router.get("/{id}")
async def get_enterprise(
    id: int,
    current_user: User = Depends(get_current_user),
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
):
    enterprise = await enterprise_service.get_by_id(id)
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return enterprise


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_enterprise(
    name: str,
    city: str,
    current_user: User = Depends(get_current_user),
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
):
    return await enterprise_service.create(name=name, city=city)


@router.put("/{id}")
async def update_enterprise(
    id: int,
    enterprise_data: EnterpriseUpdateSchema,
    current_user: User = Depends(get_current_user),
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
):
    enterprise = await enterprise_service.get_by_id(id)
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")

    manager_enterprises = await manager_enterprise_service.get_manager_enterprises(manager_id=current_user.id)
    if not any(me.enterprise_id == id for me in manager_enterprises):
        raise HTTPException(status_code=403, detail="You do not have permission to update this enterprise")

    return await enterprise_service.update(id=id, **enterprise_data.model_dump())


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_enterprise(
    id: int,
    current_user: User = Depends(get_current_user),
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
):
    enterprise = await enterprise_service.get_by_id(id)
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")

    manager_enterprises = await manager_enterprise_service.get_manager_enterprises(manager_id=current_user.id)
    if not any(me.enterprise_id == id for me in manager_enterprises):
        raise HTTPException(status_code=403, detail="You do not have permission to delete this enterprise")

    await enterprise_service.delete_by_id(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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


@router.post("/{enterprise_id}/vehicles/{vehicle_id}")
async def add_vehicle_to_enterprise(
    enterprise_id: int,
    vehicle_id: int,
    current_user: User = Depends(get_current_user),
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
):
    manager_enterprises = await manager_enterprise_service.get_manager_enterprises(manager_id=current_user.id)
    if not any(me.enterprise_id == enterprise_id for me in manager_enterprises):
        raise HTTPException(status_code=403, detail="You do not have permission to add vehicles to this enterprise")

    try:
        return await enterprise_service.add_vehicle_to_enterprise(vehicle_id=vehicle_id, enterprise_id=enterprise_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
