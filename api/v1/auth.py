from schemas.user import UserRead, UserCreate
from core.auth import fastapi_users, auth_backend
from fastapi import APIRouter


router = APIRouter()

# /login
# /logout
router.include_router(fastapi_users.get_auth_router(auth_backend))

# /register
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))

# /reset-password
router.include_router(fastapi_users.get_reset_password_router())

# /verify
router.include_router(fastapi_users.get_verify_router(UserRead))
