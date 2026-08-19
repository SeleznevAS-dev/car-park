from fastapi import APIRouter, Depends

from services.driver import DriverService, get_driver_service
from services.driver_vehicle import DriverVehicleService, get_driver_vehicle_service

router = APIRouter()


@router.get("/")
async def get_drivers(limit: int = 20, offset: int = 0, driver_service: DriverService = Depends(get_driver_service)):
    return await driver_service.get_many(limit=limit, offset=offset)


@router.get("/{id}")
async def get_driver(id: int, driver_service: DriverService = Depends(get_driver_service)):
    driver = await driver_service.get_by_id(id)
    if not driver:
        return {"error": "Driver not found"}
    return driver


@router.get("/{id}/vehicles")
async def get_driver_vehicles(
    id: int, driver_vehicle_service: DriverVehicleService = Depends(get_driver_vehicle_service)
):
    vehicles = await driver_vehicle_service.get_driver_vehicles(driver_id=id)
    return vehicles
