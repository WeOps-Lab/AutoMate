from fastapi import Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from core.http_schemas.common_response_schema import CommonResponseSchema
from server.apps.ansible.forms.playbook import PlaybookModel
from server.apps.ansible.services.playbook import AnsiblePlaybookService

playbook_api = InferringRouter()


@cbv(playbook_api)
class PlayBookAPI:
    @playbook_api.post("/fast_execute_playbook", response_model=CommonResponseSchema, name="Ansible快速执行Playbook")
    async def fast_execute_adhoc(
        self,
        data: PlaybookModel = Body(
            None,
            description="Ansible快速执行Playbook",
            example={"playbook_name": "test_mkdir", "extra_vars": {}},
        ),
    ) -> CommonResponseSchema:
        result = AnsiblePlaybookService(data)()
        return CommonResponseSchema(data=result, message="操作成功", success=True)
