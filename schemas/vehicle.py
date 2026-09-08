from pydantic import BaseModel, Field


class VehicleUpdateSchema(BaseModel):
    price: float = Field(..., ge=0)
    year: int = Field(..., ge=1900)
    mileage: int = Field(..., ge=0)
    number_of_owners: int = Field(..., ge=0)
    plate_number: str
    brand_id: int | None = None
    enterprise_id: int
