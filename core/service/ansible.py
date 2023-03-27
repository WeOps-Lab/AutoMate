from core.driver.ansible.credential import get_module_args_by_path
from core.driver.ansible.form.adhoc_result import AdHocResult
from core.driver.ansible.utils import parse_dict_to_args
from core.exception.base import AnsibleRunnerError
from core.http_schemas.ansible import CredentialRequestModel
from core.service.base import DriverService


class AnsibleService(DriverService):
    __driver_tag__ = "ansible"
    driver_run_fn = "run_adhoc"
    # 指定module
    module = ""

    def _run(self):
        adhoc_result: AdHocResult = self.driver.run_adhoc(
            module_name=self.__class__.module, module_args=parse_dict_to_args(self.input.dict())
        )
        self.output = self.output_model(**adhoc_result.result)
        if not adhoc_result.success:
            raise AnsibleRunnerError(adhoc_result.message)


class AnsibleCredentialService(AnsibleService):
    # 指定带凭据的input
    credential_input_model = CredentialRequestModel

    def __init__(self, input: credential_input_model, driver_conf: dict = None):
        super().__init__(input, driver_conf)
        self.input = self.raw_input_by_credential(input)

    def raw_input_by_credential(self, input: credential_input_model):
        credential_input = input.dict()
        if input.credential_id:
            credential_kwargs = get_module_args_by_path(self.module, input.credential_id)
            credential_input.update(credential_kwargs)
        return self.input_model(**credential_input)
