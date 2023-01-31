from typing import List

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from core.exception import handlers
from core.exception.base import AutoMateException
from core.init import init_service
from core.settings import settings


class BootStrap:
    def __init__(self, app_name: str, app_version: str, routers: List[APIRouter]):
        with open(f"{settings.base_dir}/asserts/banner.txt") as f:
            print(f.read())
        self.app_name = app_name
        self.app_version = app_version
        self.application = self._build_app()
        self.routers = routers
        self.root_router = APIRouter()

    def boot(self):
        init_service()

        self._inject_middleware()
        self._init_router()
        self._init_exception()

    def _build_app(self) -> FastAPI:
        if settings.env == "prod":
            application = FastAPI(title=self.app_name, version=self.app_version, docs_url=None, redoc_url=None)
        else:
            application = FastAPI(title=self.app_name, version=self.app_version, redoc_url=None)
        return application

    def _inject_middleware(self):
        origins = ["*"]
        self.application.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.application.add_middleware(GZipMiddleware, minimum_size=1000)
        # self.application.add_middleware(DBSessionMiddleware, db_url=settings.db_url)

    def _init_router(self):
        for r in self.routers:
            self.root_router.include_router(r)
        self.application.include_router(self.root_router, prefix="/api")

    def _init_exception(self):

        """
        修改原有异常捕获钩子,添加业务异常及全局异常捕获
        """
        # 自动化项目专属异常
        self.application.add_exception_handler(AutoMateException, handlers.automate_exception_handler)

        self.application.add_exception_handler(RequestValidationError, handlers.request_validation_exception_handler)
        self.application.add_exception_handler(HTTPException, handlers.http_exception_handler)
        self.application.add_exception_handler(Exception, handlers.all_exception_handler)
