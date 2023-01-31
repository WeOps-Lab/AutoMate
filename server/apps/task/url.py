from fastapi_utils.inferring_router import InferringRouter

from server.apps.task.api.task_api import task_api as task_v1

task_api = InferringRouter()
task_api.include_router(task_v1, prefix="/task/v1", tags=["Task"])
