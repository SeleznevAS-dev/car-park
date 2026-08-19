from fastapi import FastAPI
from sqladmin import Admin

from api.base import api_router_v1
from core.admin import add_views_to_admin
from core.database import async_session_maker

app = FastAPI()
app.include_router(api_router_v1)
admin = Admin(app, session_maker=async_session_maker)

add_views_to_admin(admin)
