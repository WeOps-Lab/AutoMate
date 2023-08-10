from core.driver.cmp.credential import get_cmp_cred_by_path
from core.service import DriverService
from server.apps.cloud.forms.cloud import CloudReqModel, CloudResultModel


class CloudService(DriverService):
    __driver_tag__ = "cmp"
    input_model = CloudReqModel
    output_model = CloudResultModel

    def __init__(self, input: input_model, driver_conf: dict = None):
        driver_conf = self.build_credential(input)
        driver_conf.update(cloud_type=input.cloud_type, region=input.region, host=input.host, project_id=None)
        super().__init__(input, driver_conf)

    def build_credential(self, input):
        credential_id = input.credential_id
        cloud_type = input.cloud_type
        credential_data = {}
        if credential_id:
            credential_data = get_cmp_cred_by_path(cloud_type, credential_id)
        return credential_data

    def _run(self):
        operate_type = self.input.operate_type
        run_kwargs = self.input.run_kwargs
        result = self.driver.run(operate_type, **run_kwargs)
        success = result.pop("result", True)
        self.output = self.output_model(result=success, data=result.get("data") if "data" in result else result)
