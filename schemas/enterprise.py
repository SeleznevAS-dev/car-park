from pydantic import BaseModel, Field


class EnterpriseUpdateSchema(BaseModel):
    name: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
