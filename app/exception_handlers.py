from fastapi import FastAPI, Request
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.responses import JSONResponse

from app.utils import parse_integrity_error


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

    @app.exception_handler(404)
    async def handle_not_found(request: Request, e: 404):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Not found!", "detail": str(e)}
        )