from core.driver.ansible.credential import get_outputs_by_path
from core.driver.ansible.form.adhoc_result import AdHocResult
from core.logger import logger
from core.service import DriverService, pre_run
from server.apps.ansible.forms.adhoc import ADHocModel


class AnsibleAdHocService(DriverService):
    __driver_tag__ = "ansible"
    driver_run_fn = "run_local_adhoc"
    input_model = ADHocModel
    output_model = AdHocResult

    @pre_run
    def build_credential_args(self):
        if self.input.credential_id:
            credential_args = get_outputs_by_path(self.input.module, self.input.credential_id)
            self.input.module_args += " " + credential_args
        logger.info(f"input:{self.input.dict()}")

    def _run(self):
        self.output = self.driver.run_local_adhoc(
            module_name=self.input.module,
            module_args=self.input.module_args,
            extravars=self.input.extra_vars,
            is_async=self.input.is_async,
            timeout=self.input.timeout,
        )
