from fastapi_utils.inferring_router import InferringRouter

from server.apps.cloud.api.cloud import cloud_api as cloud_v1
from server.apps.cloud.api.monitor import monitor_api

cloud_api = InferringRouter()
cloud_api.include_router(cloud_v1, prefix="/cloud/v1", tags=["Cloud"])
cloud_api.include_router(monitor_api, prefix="/cloud/v1/monitor", tags=["Cloud"])
