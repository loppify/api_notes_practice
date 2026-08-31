from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from app.utils.integrity_error_parser import parse_integrity_error


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(IntegrityError)
    async def handle_integrity_error(request: Request, e: IntegrityError):
        field, message = parse_integrity_error(e)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "Conflict",
                "field": field,
                "detail": message,
            },
        )

    # Обробка 404 (неіснуючі роути або HTTPException(status_code=404))
    @app.exception_handler(404)
    async def handle_not_found(request: Request, e: StarletteHTTPException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "Not Found",
                "detail": e.detail if hasattr(e, "detail") else str(e),
            },
        )

    # Обробка невалідних даних від клієнта (Body, Query, Path)
    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(
        request: Request, e: RequestValidationError
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "Validation Error", "detail": e.errors()},
        )

    # Обробка помилок у структурі відповіді бекенду
    @app.exception_handler(ResponseValidationError)
    async def handle_response_validation_error(
        request: Request, e: ResponseValidationError
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "detail": "Response format is invalid",
            },
        )
