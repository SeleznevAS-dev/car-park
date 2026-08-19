from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from models.base import ModelBase as Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"
    pass
