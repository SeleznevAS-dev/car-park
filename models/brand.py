from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import DriveType, FuelType
from models.base import ModelBase as Base

if TYPE_CHECKING:
    from models.vehicle import Vehicle


class Brand(Base):
    __tablename__ = "brands"

    brand_name: Mapped[str]
    model_name: Mapped[str]
    type: Mapped[str]
    engine_power: Mapped[float]
    engine_volume: Mapped[float]
    drive_type: Mapped[DriveType] = mapped_column(String())
    fuel_type: Mapped[FuelType] = mapped_column(String())
    load_capacity: Mapped[float]
    tank_capacity: Mapped[float]
    number_of_seats: Mapped[int]

    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="brand")

    def __str__(self):
        return f"{self.brand_name} {self.model_name}"
