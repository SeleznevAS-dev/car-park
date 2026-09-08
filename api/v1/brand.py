from fastapi import APIRouter, Depends, HTTPException

from services.brand import BrandService, get_brand_service

router = APIRouter()


@router.get("/")
async def get_brands(limit: int = 20, offset: int = 0, brand_service: BrandService = Depends(get_brand_service)):
    return await brand_service.get_many(limit=limit, offset=offset)


@router.get("/{id}")
async def get_brand(id: int, brand_service: BrandService = Depends(get_brand_service)):
    brand = await brand_service.get_by_id(id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand
