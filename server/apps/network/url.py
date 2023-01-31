from fastapi_utils.inferring_router import InferringRouter

from server.apps.network.api.ssh_api import ssh_api

network_api = InferringRouter()
network_api.include_router(ssh_api, prefix="/ssh", tags=["SSH"])
