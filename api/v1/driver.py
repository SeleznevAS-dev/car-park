from models import User
from core.auth import get_current_user
from services.manager_enterprise import ManagerEnterpriseService, get_manager_enterprise_service
from fastapi import APIRouter, Depends, HTTPException

from services.driver import DriverService, get_driver_service
from services.driver_vehicle import DriverVehicleService, get_driver_vehicle_service

router = APIRouter()


@router.get("/")
async def get_drivers(
    driver_service: DriverService = Depends(get_driver_service),
    manager_enterprise_service: ManagerEnterpriseService = Depends(get_manager_enterprise_service),
    current_user: User = Depends(get_current_user),
):
    manager_enterprises = await manager_enterprise_service.get_manager_enterprises(manager_id=current_user.id)
    if not manager_enterprises:
        return HTTPException(status_code=404, detail="Manager not found or has no enterprises")

    enterprise_ids = [me.enterprise_id for me in manager_enterprises]
    drivers = await driver_service.get_drivers_by_enterprise_ids(enterprise_ids=enterprise_ids)
    return drivers


@router.get("/{id}")
async def get_driver(id: int, driver_service: DriverService = Depends(get_driver_service)):
    driver = await driver_service.get_by_id(id)
    if not driver:
        return HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.get("/{id}/vehicles")
async def get_driver_vehicles(
    id: int, driver_vehicle_service: DriverVehicleService = Depends(get_driver_vehicle_service)
):
    vehicles = await driver_vehicle_service.get_driver_vehicles(driver_id=id)
    return vehicles
