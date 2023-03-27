from fastapi import Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from core.http_schemas.common_response_schema import CommonResponseSchema
from server.apps.ansible.forms.adhoc import ADHocModel
from server.apps.ansible.services.adhoc import AnsibleAdHocService

adhoc_api = InferringRouter()


@cbv(adhoc_api)
class AdHocAPI:
    @adhoc_api.post("/fast_execute_adhoc", response_model=CommonResponseSchema, name="Ansible快速执行Adhoc命令")
    async def fast_execute_adhoc(
        self,
        data: ADHocModel = Body(
            None,
            description="Ansible执行Adhoc命令",
            example={
                "module": "uptime",
                "module_args": "",
                "extra_vars": {},
                "inventory": [],
                "credential_id": "/host/xx",
                "is_async": False,
                "timeout": 60,
            },
        ),
    ) -> CommonResponseSchema:
        result = AnsibleAdHocService(data)()
        return CommonResponseSchema(data=result, message="操作成功", success=True)
