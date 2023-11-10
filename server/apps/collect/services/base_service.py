# -- coding: utf-8 --

# @File : base_service.py
# @Time : 2022/12/8 10:30
# @Author : windyzhao
from core.exception.base import ParamValidationError
from server.apps.collect.services.cloud_service import CloudCollectTaskManage


class BaseService(object):
    MODEL_DRIVER_MAPPING = {
        "cloud": CloudCollectTaskManage,
    }

    @classmethod
    def driver(cls, model):
        driver = cls.MODEL_DRIVER_MAPPING.get(model)
        if not driver:
            raise ParamValidationError("此模块不存在！")
        return driver
