from fastapi import APIRouter

from api.v1 import brand, driver, enterprise, vehicle, auth, manager

api_router_v1 = APIRouter(prefix="/api/v1")
api_router_v1.include_router(brand.router, prefix="/brands", tags=["brands"])
api_router_v1.include_router(vehicle.router, prefix="/vehicles", tags=["vehicles"])
api_router_v1.include_router(driver.router, prefix="/drivers", tags=["drivers"])
api_router_v1.include_router(enterprise.router, prefix="/enterprises", tags=["enterprises"])
api_router_v1.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router_v1.include_router(manager.router, prefix="/managers", tags=["managers"])
