from fastapi import Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from core.http_schemas.common_response_schema import CommonResponseSchema
from server.apps.network.forms.ssh_command import SshCommand
from server.apps.network.services.ssh_command_service import SshCommandService

ssh_api = InferringRouter()


@cbv(ssh_api)
class SshApi:
    @ssh_api.post("/v1/send_command", response_model=CommonResponseSchema, name="对网络设备执行远程命令")
    async def vcenter_cluster_info(
        self, data: SshCommand = Body(None, description="网络设备执行远程命令请求")
    ) -> CommonResponseSchema:
        service = SshCommandService()
        vcenter_result = service.execute_ssh_command(data)
        return CommonResponseSchema(data=vcenter_result, message="操作成功", success=True)
