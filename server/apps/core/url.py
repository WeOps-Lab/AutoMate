from fastapi_utils.inferring_router import InferringRouter

from server.apps.core.api.secret_api import secret_api

core_api = InferringRouter()
core_api.include_router(secret_api, prefix="/core", tags=["Core"])
