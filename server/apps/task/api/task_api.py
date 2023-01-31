# -- coding: utf-8 --

# @File : task_api.py
# @Time : 2022/11/23 18:17
# @Author : windyzhao

from fastapi import Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from core.http_schemas.common_response_schema import CommonResponseSchema
from core.tasks import task_manager

from ..forms import TaskListModel, TaskModel

task_api = InferringRouter()


@cbv(task_api)
class TaskAPI:
    @task_api.post("/status/", response_model=CommonResponseSchema, name="获取任务状态")
    async def get_task_status(
        self,
        data: TaskModel = Body(
            None,
            description="获取任务状态(可传单个task_id,或者task_id列表)",
            example={"task_id": ["0179e92f-c5ad-4d56-a3b7-20061d777b39", "0179e92f-c5ad-4d56-a3b7-20061d777b31"]},
        ),
    ) -> CommonResponseSchema:
        status = task_manager.get_task_status(data.task_id)
        return CommonResponseSchema(data=status)

    @task_api.post("/result/", response_model=CommonResponseSchema, name="获取任务结果")
    async def get_task_result(
        self,
        data: TaskModel = Body(
            None,
            description="获取任务结果(可传单个task_id,或者task_id列表)",
            example={"task_id": ["0179e92f-c5ad-4d56-a3b7-20061d777b39", "0179e92f-c5ad-4d56-a3b7-20061d777b31"]},
        ),
    ) -> CommonResponseSchema:
        status = task_manager.get_task_result(data.task_id)
        return CommonResponseSchema(data=status)

    @task_api.post("/stop_running_task/", response_model=CommonResponseSchema, name="停止运行中的任务")
    async def stop_running_task(
        self,
        data: TaskModel = Body(
            None,
            description="停止运行中的任务(可传单个task_id,或者task_id列表)",
            example={"task_id": ["0179e92f-c5ad-4d56-a3b7-20061d777b39", "0179e92f-c5ad-4d56-a3b7-20061d777b31"]},
        ),
    ) -> CommonResponseSchema:
        task_manager.stop_running_task(data.task_id)
        return CommonResponseSchema()

    @task_api.post("/", response_model=CommonResponseSchema, name="获取任务列表")
    async def get_tasks(
        self,
        data: TaskListModel = Body(
            None,
            description="获取任务列表(可过滤状态)",
            example={"status": ["STARTED"]},
        ),
    ) -> CommonResponseSchema:
        task_ids = task_manager.get_tasks(filter_status=data.status)
        return CommonResponseSchema(data=task_ids)
