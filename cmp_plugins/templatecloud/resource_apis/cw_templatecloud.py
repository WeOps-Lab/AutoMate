# -*- coding: UTF-8 -*-
import os
import random
import time

import requests

from cmp.cloud_apis.base import PrivateCloudManage
from cmp.cloud_apis.resource_client import register
from core.logger import cmp_logger as logger


def get_resource_uri(op, basic_url, **kwargs):
    if int(os.getenv("CMP_USE_MOCK", "0")):
        basic_url = "http://yapi.canway.top/mock/xx"  # mock
    return (
        {
            "get_token": "{basic_url}/get_token",
            "list_vm": "{basic_url}/instance/vms/",
            "get_monitor": "{basic_url}/instance/monitor",
        }
        .get(op, "")
        .format(basic_url=basic_url, **kwargs)
    )


def split_list(_list, count=100):
    n = len(_list)
    sublists = [_list[i : i + count] for i in range(0, n, count)]
    return sublists


def handle_request(method, url, **kwargs):
    try:
        resp = requests.request(method, url, **kwargs)
    except Exception:
        logger.exception(f"请求失败,url:{url},method:{method},kwargs:{kwargs}")
        return {"result": False, "message": f"请求失败,url:{url},method:{method},kwargs:{kwargs}", "data": {}}
    if resp.status_code > 300:
        logger.exception(
            f"请求失败,url:{url},method:{method},kwargs:{kwargs},"
            f"status_code:{resp.status_code},message:{resp.content.decode('utf-8')}"
        )
        return {
            "result": False,
            "message": f"请求错误,status_code:{resp.status_code},message:{resp.content.decode('utf-8')}",
            "data": {},
        }
    logger.info(f"请求成功,url:{url},method:{method},kwargs:{kwargs}")
    return {"result": True, "data": resp.json()}


@register
class CwTemplateCloud(object):
    def __init__(self, account, password, region="", host="", scheme="https", **kwargs):
        self.account = account
        self.password = password
        self.region = region
        self.host = host
        self.scheme = scheme
        self.kwargs = kwargs
        self.basic_url = f"{self.scheme}://{self.host}"
        self.api_version = kwargs.get("api_version", "")
        for k, v in kwargs.items():
            setattr(self, k, v)
        if self.api_version in ["x.y.z"]:
            self.cw_headers = {
                "Content-Type": "application/json;charset=UTF-8",
                "Accept": "application/json",
            }
            self.auth_token = self.login()
            self.cw_headers.update({"X-Auth-Token": self.auth_token, "Accept-Charset": "utf-8;q=1"})

        else:
            raise Exception("版本不支持,检查是否为x.y.z")

    def login(self):
        pass

    def __call__(self, *args, **kwargs):
        return getattr(self, self.name, self._non_function)(*args, **kwargs)

    @staticmethod
    def _non_function(cls, *args, **kwargs):
        return {"result": True, "data": []}

    def __getattr__(self, item):
        params = {
            "cw_headers": self.cw_headers,
            "region": self.region,
            "host": self.host,
            "account": self.account,
            "basic_url": self.basic_url,
        }
        return TemplateCloud(auth_token=self.auth_token, name=item, **params)


class TemplateCloud(PrivateCloudManage):
    """
    This class providing all operations on MANAGEONE plcatform.
    """

    def __init__(self, auth_token, name, **kwargs):
        self.auth_token = auth_token
        self.name = name
        self.cw_headers = kwargs.get("cw_headers", "")
        self.basic_url = kwargs.get("basic_url", "")
        self._handle_request = handle_request

    def __call__(self, *args, **kwargs):
        return getattr(self, self.name, self._non_function)(*args, **kwargs)

    @staticmethod
    def _non_function(cls, *args, **kwargs):
        return {"result": True, "data": []}

    def list_vms(self, **kwargs):
        """
        查询云虚机
        """
        demo = [
            {"resource_id": "123", "resource_name": "vm_test_1"},
            {"resource_id": "456", "resource_name": "vm_test_1"},
        ]
        return {"result": True, "data": demo}

    def list_hosts(self, *args, **kwargs):
        """查询宿主机"""
        pass

    def list_ds(self, *args, **kwargs):
        """查询存储设备"""
        pass

    def list_all_resources(self, **kwargs):
        demo = {"template_vms": self.list_vms(**kwargs)}
        return {"result": True, "data": demo}

    # ------------------***** monitor *****-------------------
    def get_weops_monitor_data(self, **kwargs):
        """
        Get monitor data from a specific vm.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        timestamp = int(time.time() * 1000)
        demo = {
            "123": {"cpuUsage": [(timestamp, random.uniform(0, 1))]},
            "456": {"cpuUsage": [(timestamp, random.uniform(0, 1))]},
        }
        return {"result": True, "data": demo}
