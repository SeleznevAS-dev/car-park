from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from models.base import ModelBase as Base

if TYPE_CHECKING:
    from models.driver import Driver
    from models.vehicle import Vehicle


class Enterprise(Base):
    __tablename__ = "enterprises"

    name: Mapped[str]
    city: Mapped[str]

    drivers: Mapped[list["Driver"]] = relationship(back_populates="enterprise")
    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="enterprise")

    def __str__(self):
        return f"{self.name} ({self.city})"
