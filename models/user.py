from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from models.base import ModelBase as Base

if TYPE_CHECKING:
    from models.manager import Manager


class User(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"

    manager_profile: Mapped["Manager"] = relationship(back_populates="user", uselist=False)
