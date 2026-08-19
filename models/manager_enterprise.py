from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import UniqueConstraint, ForeignKey
from models.base import AssociativeBase

if TYPE_CHECKING:
    from models.manager import Manager
    from models.enterprise import Enterprise


class ManagerEnterprise(AssociativeBase):
    __tablename__ = "manager_enterprise"

    __table_args__ = (UniqueConstraint("manager_id", "enterprise_id", name="uq_manager_enterprise"),)

    manager_id: Mapped[int] = mapped_column(ForeignKey("managers.id"), primary_key=True)
    enterprise_id: Mapped[int] = mapped_column(ForeignKey("enterprises.id"), primary_key=True)

    manager: Mapped["Manager"] = relationship(back_populates="enterprises")
    enterprise: Mapped["Enterprise"] = relationship(back_populates="managers")

    def __str__(self):
        return f"Manager ID: {self.manager_id}, Enterprise ID: {self.enterprise_id}"
