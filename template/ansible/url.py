from fastapi_utils.inferring_router import InferringRouter

from .api import api as sub_api

api = InferringRouter()
api.include_router(sub_api, prefix="/", tags=["ansible_extend"])
