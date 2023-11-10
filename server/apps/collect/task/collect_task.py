# -- coding: utf-8 --

# @File : collect_task.py
# @Time : 2022/12/8 10:10
# @Author : windyzhao

from core.celery_app import celery_app as celery
from server.apps.collect.services.base_service import BaseService
from server.apps.collect.task.collect_callback import CollectTaskCallback


@celery.task(bind=True, base=CollectTaskCallback)
def collect_task(self, params):
    driver = params["driver"]
    driver = BaseService.driver(driver)
    bulk_exec = driver(params, self.request.id)
    return bulk_exec.main()


def test_collect_task(params):
    driver = params["driver"]
    driver = BaseService.driver(driver)
    bulk_exec = driver(params, "测试id")
    return bulk_exec.main()
