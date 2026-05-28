from fastapi import HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse, Response
from typing import Generic, TypeVar, Optional
from datetime import datetime


T = TypeVar("T")


class HttpResponseMessages:
    SUCCESS = "Success"
    CREATED = "Resource created"
    NO_CONTENT = "No content"
    UPDATED = "Resource updated"
    NOT_FOUND = "Resource not found"
    UNAUTHORIZED = (
        "User is not authorized to access this resource with an explicit deny"
    )
    FORBIDDEN = "Forbidden"
    INTERNAL_SERVER_ERROR = "Internal server error"
    BAD_REQUEST = "Bad request"
    UNPROCESSABLE_ENTITY = "Unprocessable entity"
    CONFLICT = "Resource conflict"
    RATE_LIMITED = "Too many requests"


class HttpStatus:
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    RATE_LIMITED = 429
    INTERNAL_SERVER_ERROR = 500


class PaginationType(BaseModel):
    count: int
    currentPage: int
    nextPage: Optional[int] = None
    prevPage: Optional[int] = None
    lastPage: int


class CoffeeAppResponseModel(BaseModel, Generic[T]):
    status: int
    statusMessage: str
    data: Optional[T] = None
    pagination: Optional[PaginationType] = None
    timestamp: Optional[str] = None
    error: Optional[dict] = None


class CoffeeAppHttpResponse(Generic[T]):
    @staticmethod
    def ok(data: T, pagination: Optional[PaginationType] = None, message: str = HttpResponseMessages.SUCCESS) -> JSONResponse:
        content = {
            "status": HttpStatus.OK,
            "statusMessage": message,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
        }

        if isinstance(data, list):
            content["pagination"] = pagination.model_dump() if pagination else None

        return JSONResponse(
            status_code=HttpStatus.OK,
            content=content,
        )

    @staticmethod
    def created(data: T, message: str = HttpResponseMessages.CREATED) -> JSONResponse:
        return JSONResponse(
            status_code=HttpStatus.CREATED,
            content={
                "status": HttpStatus.CREATED,
                "statusMessage": message,
                "data": data,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @staticmethod
    def no_content() -> Response:
        return Response(status_code=HttpStatus.NO_CONTENT)

    @staticmethod
    def updated(data: Optional[T] = None, message: str = HttpResponseMessages.UPDATED) -> JSONResponse:
        return JSONResponse(
            status_code=HttpStatus.OK,
            content={
                "status": HttpStatus.OK,
                "statusMessage": message,
                "data": data,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @staticmethod
    def not_found(
        data: Optional[T] = None, error_id: Optional[str] = None
    , message: Optional[str] = None) -> HTTPException:
        raise HTTPException(
            status_code=HttpStatus.NOT_FOUND,
            detail={
                "status": HttpStatus.NOT_FOUND,
                "statusMessage": message or HttpResponseMessages.NOT_FOUND,
                "error": {
                    "code": error_id or "NOT_FOUND",
                    "data": data,
                },
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @staticmethod
    def unauthorized(message: Optional[str] = None) -> HTTPException:
        raise HTTPException(
            status_code=HttpStatus.UNAUTHORIZED,
            detail={
                "status": HttpStatus.UNAUTHORIZED,
                "statusMessage": message or HttpResponseMessages.UNAUTHORIZED,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @staticmethod
    def unauthorized_with_code(error_id: Optional[str] = None, message: Optional[str] = None) -> HTTPException:
        raise HTTPException(
            status_code=HttpStatus.UNAUTHORIZED,
            detail={
                "status": HttpStatus.UNAUTHORIZED,
                "statusMessage": message or HttpResponseMessages.UNAUTHORIZED,
                "error": {
                    "code": error_id or "UNAUTHORIZED",
                    "data": None,
                },
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @staticmethod
    def forbidden(
        data: Optional[T] = None, error_id: Optional[str] = None
    , message: Optional[str] = None) -> HTTPException:
        raise HTTPException(
            status_code=HttpStatus.FORBIDDEN,
            detail={
                "status": HttpStatus.FORBIDDEN,
                "statusMessage": message or HttpResponseMessages.FORBIDDEN,
                "error": {
                    "code": error_id or "FORBIDDEN",
                    "data": data,
                },
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @staticmethod
    def internal_error(message: Optional[str] = None) -> HTTPException:
        raise HTTPException(
            status_code=HttpStatus.INTERNAL_SERVER_ERROR,
            detail={
                "status": HttpStatus.INTERNAL_SERVER_ERROR,
                "statusMessage": message or HttpResponseMessages.INTERNAL_SERVER_ERROR,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @staticmethod
    def bad_request(data: Optional[T] = None, error_id: Optional[str] = None, message: Optional[str] = None) -> HTTPException:
        raise HTTPException(
            status_code=HttpStatus.BAD_REQUEST,
            detail={
                "status": HttpStatus.BAD_REQUEST,
                "statusMessage": message or HttpResponseMessages.BAD_REQUEST,
                "error": {
                    "code": error_id or "BAD_REQUEST",
                    "data": data,
                },
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @staticmethod
    def conflict(data: Optional[T] = None, error_id: Optional[str] = None, message: Optional[str] = None) -> HTTPException:
        raise HTTPException(
            status_code=HttpStatus.CONFLICT,
            detail={
                "status": HttpStatus.CONFLICT,
                "statusMessage": message or HttpResponseMessages.CONFLICT,
                "error": {
                    "code": error_id or "CONFLICT",
                    "data": data,
                },
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @staticmethod
    def unprocessable_entity(data: Optional[T] = None, error_id: Optional[str] = None, message: Optional[str] = None) -> HTTPException:
        raise HTTPException(
            status_code=HttpStatus.UNPROCESSABLE_ENTITY,
            detail={
                "status": HttpStatus.UNPROCESSABLE_ENTITY,
                "statusMessage": message or HttpResponseMessages.UNPROCESSABLE_ENTITY,
                "error": {
                    "code": error_id or "UNPROCESSABLE_ENTITY",
                    "data": data,
                },
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @staticmethod
    def rate_limited(message: Optional[str] = None) -> HTTPException:
        raise HTTPException(
            status_code=HttpStatus.RATE_LIMITED,
            detail={
                "status": HttpStatus.RATE_LIMITED,
                "statusMessage": message or HttpResponseMessages.RATE_LIMITED,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )
