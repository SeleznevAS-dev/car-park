from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import ModelBase as Base
from models.driver_vehicle import DriverVehicle

if TYPE_CHECKING:
    from models.brand import Brand
    from models.enterprise import Enterprise


class Vehicle(Base):
    __tablename__ = "vehicles"

    price: Mapped[float]
    year: Mapped[int]
    mileage: Mapped[int]
    number_of_owners: Mapped[int]
    plate_number: Mapped[str] = mapped_column(unique=True)

    brand_id: Mapped[int | None] = mapped_column(ForeignKey("brands.id"))
    brand: Mapped[Brand | None] = relationship(back_populates="vehicles")

    enterprise_id: Mapped[int] = mapped_column(ForeignKey("enterprises.id"))
    enterprise: Mapped[Enterprise] = relationship(back_populates="vehicles")

    drivers: Mapped[List["DriverVehicle"]] = relationship(back_populates="vehicle")

    def __str__(self):
        return f"{self.plate_number}"
