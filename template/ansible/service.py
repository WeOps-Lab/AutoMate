from core.service import DriverService

from .form import RequestModel, ResultModel


class ModuleService(DriverService):
    __driver_tag__ = "ansible"
    driver_run_fn = "run_adhoc"
    input_model = RequestModel
    output_model = ResultModel

    def _run(self):
        self.output = self.driver.run_adhoc(module_name="module_name", module_args=self.input.dict())
