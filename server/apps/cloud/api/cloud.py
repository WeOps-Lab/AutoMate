from fastapi import Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from core.http_schemas.common_response_schema import CommonResponseSchema

from ..forms.cloud import CloudReqModel, CloudResultModel
from ..services.cloud import CloudService

cloud_api = InferringRouter()


@cbv(cloud_api)
class CloudAPI:
    @cloud_api.post("/run/", response_model=CommonResponseSchema, name="通用云服务操作(增删改查)")
    async def get_cloud_status(
        self,
        data: CloudReqModel = Body(
            None,
            description="通用云服务操作(增删改查)",
            example={
                "cloud_type": "aliyun",
                "operate_type": "list_vms",
                "region": "cn-guangzhou",
                "credential_id": "test_cmp/aliyun_1",
                "run_kwargs": {},
            },
        ),
    ) -> CommonResponseSchema:
        result: CloudResultModel = CloudService(data)()
        return CommonResponseSchema(data=result)
