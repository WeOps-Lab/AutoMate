# -- coding: utf-8 --

# @File : collect_callback.py
# @Time : 2022/12/8 10:11
# @Author : windyzhao
import json

import requests

from core.logger import collect_logger as logger
from core.settings import settings
from core.tasks import BaseCallback


class CollectTaskCallback(BaseCallback):
    """
    #方法相关的参数
    exc:失败时的错误的类型；
    task_id:任务的id；
    args:任务函数的参数；
    kwargs:键值对参数；
    einfo:失败或重试时的异常详细信息；
    retval:任务成功执行的返回值；
    """

    # 任务失败时执行
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        super().on_failure(exc, task_id, args, kwargs, einfo)
        self.callback_weops(
            task_id=task_id,
            success=False,
            message="celery任务ansible_task执行失败！exc={}, einfo={}".format(exc, einfo),
            data=[],
        )

    # 任务成功时执行
    def on_success(self, retval, task_id, args, kwargs):
        super().on_success(retval, task_id, args, kwargs)
        self.callback_weops(task_id=task_id, success=True, message="celery任务ansible_task任务成功！", data=retval)

    @staticmethod
    def callback_weops(task_id, data, success: bool = True, message: str = ""):
        headers = {}
        url = f"{settings.weops_path}/{settings.ansible_callback}/"
        try:
            resp = requests.post(
                url=url,
                data=json.dumps({"success": success, "task_id": task_id, "data": data, "message": message}),
                headers=headers,
                verify=False,
            )
            try:
                resp_json = resp.json()
                logger.info("celery任务ansible_task任务回调weops完成!, task_id={}, resp_json={}".format(task_id, resp_json))
            except Exception as json_e:
                logger.error("weops回调json解析出错！error={}".format(json_e))
        except Exception as err:
            logger.warning("celery任务ansible_task任务回调weops失败!, task_id={}, error:{}".format(task_id, err))
