from schemas.vehicle import VehicleUpdateSchema
from services.manager_enterprise import ManagerEnterpriseService, get_manager_enterprise_service
from models import User
from core.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status

from services.driver_vehicle import DriverVehicleService, get_driver_vehicle_service
from services.vehicle import VehicleService, get_vehicle_service

router = APIRouter()


@router.get("/")
async def get_vehicles(
    limit: int = 20,
    offset: int = 0,
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    current_user: User = Depends(get_current_user),
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
):
    manager_enterprises = await manager_enterprise_service.get_manager_enterprises(manager_id=current_user.id)
    if not manager_enterprises:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manager not found or has no enterprises")

    enterprise_ids = [me.enterprise_id for me in manager_enterprises]
    vehicles = []
    for enterprise_id in enterprise_ids:
        vehicles.extend(
            await vehicle_service.get_by_enterprise_id(enterprise_id=enterprise_id, limit=limit, offset=offset)
        )

    return vehicles


@router.put("/{id}")
async def update_vehicle(
    id: int,
    vehicle_data: VehicleUpdateSchema,
    current_user: User = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
):
    vehicle = await vehicle_service.get_by_id(id)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    manager_enterprises = await manager_enterprise_service.get_manager_enterprises(manager_id=current_user.id)
    allowed_enterprise_ids = {me.enterprise_id for me in manager_enterprises}

    if vehicle.enterprise_id not in allowed_enterprise_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to manage this vehicle"
        )

    if vehicle_data.enterprise_id not in allowed_enterprise_ids:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot move vehicle to this enterprise")

    return await vehicle_service.update(id=id, **vehicle_data.model_dump())


@router.delete("/{id}")
async def delete_vehicle(
    id: int,
    current_user: User = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
):
    vehicle = await vehicle_service.get_by_id(id)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    manager_enterprises = await manager_enterprise_service.get_manager_enterprises(manager_id=current_user.id)
    allowed_enterprise_ids = {me.enterprise_id for me in manager_enterprises}

    if vehicle.enterprise_id not in allowed_enterprise_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to manage this vehicle"
        )

    return await vehicle_service.delete_by_id(id=id)


@router.get("/{id}")
async def get_vehicle_by_id(id: int, vehicle_service: VehicleService = Depends(get_vehicle_service)):
    vehicle = await vehicle_service.get_by_id(id)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return vehicle


@router.get("/{id}/drivers")
async def get_vehicle_drivers(
    id: int, driver_vehicle_service: DriverVehicleService = Depends(get_driver_vehicle_service)
):
    drivers = await driver_vehicle_service.get_vehicle_drivers(vehicle_id=id)
    return drivers
