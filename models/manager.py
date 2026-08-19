from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from models.base import ModelBase as Base

if TYPE_CHECKING:
    from models.user import User
    from models.manager_enterprise import ManagerEnterprise


class Manager(Base):
    __tablename__ = "managers"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="manager_profile", uselist=False)

    enterprises: Mapped[list["ManagerEnterprise"]] = relationship(back_populates="manager")
