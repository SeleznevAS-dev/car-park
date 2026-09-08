from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_users.router.common import ErrorCode


def _add_validation_exception_handler(app):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = exc.errors()

        invalid_body = any(
            error["type"] == "json_invalid" or (error["loc"] == ("body",) and isinstance(error.get("input"), bytes))
            for error in errors
        )

        status_code = 400 if invalid_body else 422

        return JSONResponse(status_code=status_code, content={"detail": jsonable_encoder(errors)})


def _add_bad_credentials_exception_handler(app):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        status_code = 401 if exc.detail == ErrorCode.LOGIN_BAD_CREDENTIALS else exc.status_code
        return JSONResponse(status_code=status_code, content={"detail": exc.detail})


def add_handlers(app):
    _add_validation_exception_handler(app)
    _add_bad_credentials_exception_handler(app)
