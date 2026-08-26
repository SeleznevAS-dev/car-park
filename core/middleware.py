from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi_csrf_protect import CsrfProtect


class CsrfMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return await call_next(request)

        csrf_protect = CsrfProtect()

        try:
            await csrf_protect.validate_csrf(request)
        except CsrfProtectError as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.message})

        return await call_next(request)


def add_middlewares(app):
    app.add_middleware(CsrfMiddleware)
