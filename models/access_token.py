from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from models.base import ModelBase as Base


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[int]):
    __tablename__ = "access_tokens"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False)
