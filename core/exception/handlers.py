import traceback

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR

from core.exception.base import AutoMateException
from core.logger import logger


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    headers = getattr(exc, "headers", None)
    if headers:
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code, headers=headers)
    else:
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.error(f"全局异常\nURL:{request.url}\nHeaders:{request.headers}\nmessage:{exc}\n{traceback.format_exc()}")

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=dict(
            data=jsonable_encoder(exc.errors()),
            result=False,
            code=str(HTTP_422_UNPROCESSABLE_ENTITY * 1000),
            msg=str(exc),
        ),
    )


async def automate_exception_handler(request: Request, exc: AutoMateException) -> JSONResponse:
    logger.error(f"全局异常\nURL:{request.url}\nHeaders:{request.headers}\nmessage:{exc.message}\n{traceback.format_exc()}")
    return JSONResponse(status_code=exc.status_code, content=exc.response_data())


async def all_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"全局异常\nURL:{request.url}\nHeaders:{request.headers}\nmessage:{repr(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=dict(result=False, code=str(HTTP_500_INTERNAL_SERVER_ERROR * 1000), message="系统异常,请联系管理员处理", data=None),
    )
