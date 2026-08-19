from fastapi import APIRouter, Depends, HTTPException, status

from services.driver_vehicle import DriverVehicleService, get_driver_vehicle_service
from services.vehicle import VehicleService, get_vehicle_service

router = APIRouter()


@router.get("/")
async def get_vehicles(
    limit: int = 20, offset: int = 0, vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    return await vehicle_service.get_many(limit=limit, offset=offset)


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
