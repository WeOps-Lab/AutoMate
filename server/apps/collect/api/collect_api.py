# -- coding: utf-8 --

# @File : collect_api.py
# @Time : 2022/12/8 09:48
# @Author : windyzhao
import datetime

from fastapi import Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from core.http_schemas.common_response_schema import CommonResponseSchema
from core.settings import settings
from server.apps.collect.forms.collect_forms import CollectTaskModel
from server.apps.collect.task.collect_task import collect_task, test_collect_task

collect_api = InferringRouter()


@cbv(collect_api)
class CollectTaskApi:
    @collect_api.post("/v1/run_collect_task", response_model=CommonResponseSchema, name="快速执行采集任务")
    async def collect_task(
        self,
        data: CollectTaskModel = Body(
            None,
            description="快速执行采集任务",
            example={
                "module": "list_vms",
                "driver": "cloud",
                "bk_obj_id": "aliyun_ecs",
                "credential": ["sssss"],
                "classification": "aliyun",
                "context": {},
            },
        ),
    ) -> CommonResponseSchema:
        expires = datetime.timedelta(hours=settings.celery_task_expires) + datetime.datetime.now()  # 6小时超时时间
        task = collect_task.apply_async(args=(data.dict(),), expires=expires)
        return CommonResponseSchema(data=task.task_id, message="操作成功", success=True)

    @collect_api.post("/v1/collect_task_test", response_model=CommonResponseSchema, name="开发测试快速执行采集任务")
    async def collect_task_test(
        self,
        data: CollectTaskModel = Body(
            None,
            description="快速执行采集任务",
            example={
                "module": "list_vms",
                "driver": "cloud",
                "bk_obj_id": "aliyun_ecs",
                "credential": ["sssss"],
                "classification": "aliyun",
                "context": {},
            },
        ),
    ) -> CommonResponseSchema:
        result = test_collect_task(data.dict())
        return CommonResponseSchema(data=result, message="操作成功", success=True)
