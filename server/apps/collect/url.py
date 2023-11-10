from fastapi_utils.inferring_router import InferringRouter

from server.apps.collect.api.collect_api import collect_api

coll_api = InferringRouter()
coll_api.include_router(collect_api, prefix="/collect", tags=["Collect"])
