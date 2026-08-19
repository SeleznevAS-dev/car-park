from fastapi import APIRouter, Depends

from services.enterprise import EnterpriseService, get_enterprise_service

router = APIRouter()


@router.get("/")
async def get_enterprises(
    limit: int = 20, offset: int = 0, enterprise_service: EnterpriseService = Depends(get_enterprise_service)
):
    return await enterprise_service.get_many(limit=limit, offset=offset)


@router.get("/{id}")
async def get_enterprise(id: int, enterprise_service: EnterpriseService = Depends(get_enterprise_service)):
    enterprise = await enterprise_service.get_by_id(id)
    if not enterprise:
        return {"error": "Enterprise not found"}
    return enterprise
