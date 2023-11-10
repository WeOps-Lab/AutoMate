import uvicorn

from core.bootstrap import BootStrap
from core.settings import settings
from server.apps.ansible.url import ansible_api
from server.apps.cloud.url import cloud_api
from server.apps.collect.url import coll_api as collect_api
from server.apps.core.url import core_api
from server.apps.network.url import network_api
from server.apps.task.url import task_api

bootstrap = BootStrap(
    app_name="Auto-Mate",
    app_version="0.1.0",
    routers=[
        network_api,
        core_api,
        ansible_api,
        collect_api,
        task_api,
        cloud_api,
    ],
)
bootstrap.boot()

if __name__ == "__main__":
    if settings.env == "dev":
        uvicorn.run(
            app="main:bootstrap.application", host=settings.app_host, port=settings.app_port, reload=True, debug=True
        )
    else:
        uvicorn.run(
            app="main:bootstrap.application",
            host=settings.app_host,
            port=settings.app_port,
            reload=False,
            debug=False,
            log_level="info",
        )
