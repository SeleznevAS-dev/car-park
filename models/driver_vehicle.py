from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import AssociativeBase

if TYPE_CHECKING:
    from models.driver import Driver
    from models.vehicle import Vehicle


class DriverVehicle(AssociativeBase):
    __tablename__ = "driver_vehicle"

    __table_args__ = (UniqueConstraint("driver_id", "vehicle_id"),)

    is_active: Mapped[bool] = mapped_column(default=False)

    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"), primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), primary_key=True)

    driver: Mapped["Driver"] = relationship(back_populates="vehicles")
    vehicle: Mapped["Vehicle"] = relationship(back_populates="drivers")

    def __str__(self):
        return f"Driver ID: {self.driver_id}, Vehicle ID: {self.vehicle_id}, Active: {self.is_active}"
