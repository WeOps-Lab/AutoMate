from fastapi import Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from core.http_schemas.common_response_schema import CommonResponseSchema

from .form import RequestModel, ResponseModel
from .service import ModuleService

api = InferringRouter()


@cbv(api)
class ModuleAPI:
    @api.post("/module_name", response_model=CommonResponseSchema, name="module_desc")
    async def fast_execute_adhoc(
        self,
        data: RequestModel = Body(
            None,
            description="module_desc",
        ),
    ) -> CommonResponseSchema:
        result: ResponseModel = ModuleService(data)()
        return CommonResponseSchema(data=result, message="操作成功", success=True)
