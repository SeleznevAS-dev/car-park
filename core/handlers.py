from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_csrf_protect.exceptions import CsrfProtectError


def _add_csrf_exception_handler(app):
    @app.exception_handler(CsrfProtectError)
    async def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


def add_handlers(app):
    _add_csrf_exception_handler(app)
