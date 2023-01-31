from fastapi_utils.inferring_router import InferringRouter

from server.apps.ansible.api.adhoc import adhoc_api
from server.apps.ansible.api.playbook import playbook_api

ansible_api = InferringRouter()
ansible_api.include_router(adhoc_api, prefix="/ansible/v1", tags=["Ansible"])
ansible_api.include_router(playbook_api, prefix="/ansible/v1", tags=["Ansible"])
