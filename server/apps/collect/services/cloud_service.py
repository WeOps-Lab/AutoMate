# -- coding: utf-8 --

# @File : cloud_service.py
# @Time : 2022/12/8 11:10
# @Author : windyzhao
from core.db.redis_client import get_redis_client
from core.driver.cmp.credential import get_cmp_cred_by_path
from core.format import format_util
from core.logger import collect_logger as logger
from core.service import DriverService
from core.settings import settings
from core.utils.threadpool import THREAD_COUNT_KEY
from server.apps.cloud.forms.cloud import CloudResultModel


class CollectCloudService(DriverService):
    __driver_tag__ = "cmp"
    output_model = CloudResultModel

    def _run(self):
        operate_type = self.input["operate_type"]
        result = self.driver.run(operate_type)
        success = result.pop("result", True)
        self.output = self.output_model(result=success, data=result.get("data") if "data" in result else result)


class CloudCollectTaskManage(object):
    def __init__(self, params: dict, task_id: str):
        self.task_id = task_id
        self.params = params
        self.context = self.params["context"]
        self.bk_inst_name = self.context["bk_inst_name"]
        self.module = self.params["module"]
        self.bk_obj_id = self.params["bk_obj_id"]
        self.credential = self.params["credential"]
        self.classification = self.params["classification"]
        self.region_ids = self.context["regions"]
        self.host = self.context.get("host")
        self.operate_type = params.get("module", "list_vms")
        self.task_key = THREAD_COUNT_KEY.format(**{"task_uuid": self.task_id})
        self.cloud_type, self.account = self.get_cloud_type_account()

    def get_cloud_type_account(self):
        _cloud_type = self.bk_obj_id.split("_", 1)[0]
        account = f"{_cloud_type}_account"
        if self.bk_obj_id == "mo_server":
            _cloud_type = "manageone"
        return _cloud_type, account

    def get_input(self):
        # 从format input 中获取格式化好.的数据 如凭据
        input = {"operate_type": self.operate_type, "cloud_type": self.cloud_type}
        driver_conf = self.build_credential()
        driver_conf.update(cloud_type=self.cloud_type, region=None, project_id=None)
        if self.host:
            driver_conf.update(host=self.host)
        return input, driver_conf

    def format_output(self, result):
        # 根据采集返回的数据，格式化返回的采集数据
        context = {
            "bk_obj_id": self.bk_obj_id,
            "task_id": self.task_id,
            "bk_inst_name": self.bk_inst_name,
            "account_name": self.bk_inst_name,
        }
        output = format_util.format_cmp_collect(self.cloud_type, result, context=context)
        # 组装bk_inst_name
        for _output in output:
            _output[self.account] = self.bk_inst_name
            self.add_access_point(_output)
        return output

    def get_cloud_vm(self):
        result = []
        input, driver_conf = self.get_input()
        with get_redis_client(settings.redis_url) as redis_client:
            redis_client.hset(self.task_key, "all", len(self.region_ids))
        if self.region_ids:
            for region_id in self.region_ids:
                input["region"] = region_id
                driver_conf["region"] = region_id
                self.collect(input, driver_conf, result)
        else:
            self.collect(input=input, driver_conf=driver_conf, result=result)

        return result

    def collect(self, input, driver_conf, result):
        output = CollectCloudService(input=input, driver_conf=driver_conf)()
        with get_redis_client(settings.redis_url) as redis_client:
            redis_client.hincrby(self.task_key, "finish", 1)
            if output.result:
                format_output = self.format_output(output.data)
                result.extend(format_output)
                redis_client.hincrby(self.task_key, "success", 1)
            else:
                logger.warning(
                    "cloud collect error! input={}, region={}, message={}.".format(
                        input, input.get("region", "无"), output.message
                    )
                )

    def build_credential(self) -> dict:
        credential_data = {}
        if self.credential:
            credential_data = get_cmp_cred_by_path(self.cloud_type, self.credential[0])
        return credential_data

    @staticmethod
    def add_access_point(result: dict):
        """
        加上access_point 接入点
        @param result:
        @return:
        """
        access_point = settings.access_point
        result.update({"access_point": access_point})

    def main(self):
        result = self.get_cloud_vm()
        return result
