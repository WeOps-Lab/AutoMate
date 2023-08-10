import copy
import time
import typing

from fastapi import Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from core.driver.cmp.credential import get_cmp_cred_by_path
from core.http_schemas.common_response_schema import CommonResponseSchema
from core.pusher import prom_pusher

from ..forms.monitor import MetricModel, MonitorReqModel
from ..tasks.monitor import get_and_push_monitor

monitor_api = InferringRouter()


@cbv(monitor_api)
class CloudAPI:
    @monitor_api.post("/monitor_collect/", response_model=CommonResponseSchema, name="监控采集(CMP)")
    async def monitor_collect(
        self,
        data: MonitorReqModel = Body(
            None,
            description="监控采集(CMP)",
            example={
                "cloud_type": "qcloud",
                "resources": [
                    {
                        "bk_obj_id": "qcloud_cvm",
                        "bk_inst_id": 111,
                        "resource_id": "ins-qnopai6m",
                        "bk_inst_name": "深信服",
                        "bk_biz_id": 2,
                    },
                    {
                        "bk_obj_id": "qcloud_cvm",
                        "bk_inst_id": 222,
                        "resource_id": "ins-0g4ehetc",
                        "bk_inst_name": "autopack",
                        "bk_biz_id": 2,
                    },
                ],
                "start_time": "2022-12-12 14:10:00",
                "end_time": "2022-12-12 14:15:00",
                "host": "",
                "region": "",
                "credential_id": "test_cmp/qcloud_1",
                "metrics": [
                    "CPUUsage",
                    "MemUsed",
                    "MemUsage",
                    "CvmDiskUsage",
                    "LanOuttraffic",
                    "LanIntraffic",
                    "LanOutpkg",
                    "LanInpkg",
                    "WanOuttraffic",
                    "WanIntraffic",
                    "WanOutpkg",
                    "WanInpkg",
                ],
                "period": 300,
            },
        ),
    ) -> CommonResponseSchema:
        credential_id = data.credential_id
        cloud_type = data.cloud_type
        credential_data = {}
        if credential_id:
            credential_data = get_cmp_cred_by_path(cloud_type, credential_id)
        kwargs = data.dict()
        kwargs.pop("credential_id")
        kwargs.update(credential_data)
        get_and_push_monitor.delay(**kwargs)
        return CommonResponseSchema()

    @monitor_api.post("/push_metrics/", response_model=CommonResponseSchema, name="监控上报")
    async def push_metrics(
        self,
        metrics: typing.List[MetricModel] = Body(
            ...,
            description="监控上报",
            example=[
                {
                    "name": "内存使用率",
                    "key": "memoryUsage",
                    "value": 0.6,
                    "dims": None,
                    "bk_biz_id": 2,
                    "protocol": "database",
                    "bk_obj_id": "mysql",
                    "bk_inst_id": 10,
                    "bk_inst_name": "mysql-1",
                    "resource_id": "234",
                },
                {
                    "name": "磁盘使用率",
                    "key": "Diskusage",
                    "value": "0.2",
                    "dims": [{"name": "挂载点", "key": "mount_point", "value": "/data"}],
                    "bk_biz_id": 2,
                    "protocol": "database",
                    "bk_obj_id": "mysql",
                    "bk_inst_id": 12,
                    "bk_inst_name": "mysql-2",
                    "resource_id": "456",
                },
            ],
        ),
    ) -> CommonResponseSchema:
        timestamp = int(time.time() * 1000)
        metric_list = []
        for metric in metrics:
            metric_item = [
                timestamp,
                metric.key,
                {
                    "bk_obj_id": metric.bk_obj_id,
                    "bk_inst_id": metric.bk_inst_id and str(metric.bk_inst_id),
                    "bk_inst_name": metric.bk_inst_name,
                    "bk_biz_id": metric.bk_biz_id and str(metric.bk_biz_id),
                    "instanceId": metric.resource_id,
                    "protocol": f"custom_{metric.protocol or 'other'}",
                    "source": "automate",
                },
                metric.value,
            ]
            for dim in metric.dims or []:
                metric_item[2].update({dim.key: dim.value})
            metric_dict = copy.copy(metric_item[2])
            for k, v in metric_dict.items():
                if v is None:
                    metric_item[2].pop(k)
            metric_list.append(tuple(metric_item))
        await prom_pusher.mpush(metric_list)
        return CommonResponseSchema()
