from fastapi_csrf_protect import CsrfProtect
from schemas.user import UserRead, UserCreate
from core.auth import fastapi_users, auth_backend
from fastapi import APIRouter, Depends, Response


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


# /csrf-token
@router.get("/csrf-token")
async def get_csrf_token(csrf_protect: CsrfProtect = Depends()):
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    response = Response(
        content=csrf_token,
        media_type="text/plain",
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response
