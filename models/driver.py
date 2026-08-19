from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import ModelBase as Base
from models.driver_vehicle import DriverVehicle

if TYPE_CHECKING:
    from models.enterprise import Enterprise


class Driver(Base):
    __tablename__ = "drivers"

    name: Mapped[str]
    surname: Mapped[str]
    salary: Mapped[int]
    driver_experience: Mapped[float]

    enterprise_id: Mapped[int] = mapped_column(ForeignKey("enterprises.id"))
    enterprise: Mapped["Enterprise"] = relationship(back_populates="drivers")

    vehicles: Mapped[List["DriverVehicle"]] = relationship(back_populates="driver")

    def __str__(self):
        return f"{self.name} {self.surname}"

    @property
    def vehicle_ids(self) -> list[int]:
        return [dv.vehicle_id for dv in self.vehicles]
