import json
import time
import typing

from celery.result import AsyncResult
from kombu.utils.functional import maybe_list

from core.celery_app import celery_app as celery
from core.db.redis_client import get_redis_client
from core.logger import logger


class TaskManager:
    @staticmethod
    def apply_async(task: typing.Any, task_args: tuple = (), task_kwargs: dict = None, **kwargs):
        """

        :param task: @task的function
        :param task_args: tuple or list
        :param task_kwargs: dict
        :param kwargs:  还可以配置超时:expires;延迟执行:eta;重试:retry
        :return:
        """
        if not isinstance(task, celery.Task):
            raise Exception("task is not a celery task ; must register task to celery ")
        task_kwargs = task_kwargs or {}
        async_result = task.apply_async(task_args, task_kwargs, **kwargs)
        return async_result.task_id

    @staticmethod
    def get_attr(obj, attr):
        value = getattr(obj, attr)
        if isinstance(value, Exception):
            value = repr(value)
        return value

    @staticmethod
    def _wrapper_async_result(task_id: typing.Union[str, typing.List[str]], attr: str):
        if isinstance(task_id, str):
            return TaskManager.get_attr(AsyncResult(task_id), attr)
        elif isinstance(task_id, list):
            attr_value = {}
            for _task_id in task_id:
                attr_value[_task_id] = TaskManager.get_attr(AsyncResult(_task_id), attr)
            return attr_value
        raise TypeError("task_id must be a str or list")

    @staticmethod
    def get_task_status(task_id: typing.Union[str, typing.List[str]]) -> typing.Union[str, typing.Dict[str, str]]:
        return TaskManager._wrapper_async_result(task_id, "status")

    @staticmethod
    def get_task_result(task_id: typing.Union[str, typing.List[str]]) -> typing.Union[str, typing.Dict]:
        return TaskManager._wrapper_async_result(task_id, "result")

    @staticmethod
    def get_backend_client():
        backend = celery.conf["CELERY_RESULT_BACKEND"]
        if backend.startswith("redis"):
            backend_client = get_redis_client(backend)
        else:
            raise Exception(f"backend is not redis backend:{backend}")
        return backend_client

    @staticmethod
    def get_task_keyprefix():
        return celery.backend.task_keyprefix.decode()

    @staticmethod
    def get_tasks(filter_status: typing.Optional[typing.List[str]] = None) -> typing.List[str]:
        """

        :param filter_status: ["PENDING","STARTED","SUCCESS","FAILURE","RETRY","REVOKED"] 可选其一或多个,默认__all__
        :return:task_id列表
        """
        backend_client = TaskManager.get_backend_client()
        task_keyprefix = TaskManager.get_task_keyprefix()
        task_ids = backend_client.keys(f"{task_keyprefix}*")
        task_ids = [task_id.replace(task_keyprefix, "") for task_id in task_ids]

        if filter_status:
            task_ids = list(filter(lambda x: TaskManager.get_task_status(x) in filter_status, task_ids))
        return task_ids

    @staticmethod
    def stop_running_task(task_id: typing.Union[str, typing.List[str]], force_change_status=False):
        """

        :param task_id:
        :param force_change_status: 是否强制修改状态,由于worker被莫名kill导致,只能通过洗库控制状态把STARTED变成REVOKED
        :return:
        """
        # 默认signal = SIGTERM 热终止 (暴力可用SIGQUIT 冷终止 ,如终止需要其他操作可以使用SIGUSR1捕获异常SoftTimeLimitExceeded)
        task_ids = maybe_list(task_id)
        celery.control.revoke(task_ids, terminate=True)
        started_task_ids = list(set(TaskManager.get_tasks(["STARTED"])) & set(task_ids))

        if force_change_status and started_task_ids:
            backend_client = TaskManager.get_backend_client()
            task_keyprefix = TaskManager.get_task_keyprefix()
            keys = [f"{task_keyprefix}{task_id}" for task_id in task_ids]
            with backend_client.pipeline() as p:
                p.mget(keys)
                values = p.execute()[0]
                key_values = {}
                for index, value in enumerate(values):
                    value = json.loads(value)
                    value["status"] = "REVOKED"
                    value["result"] = None
                    key_values[keys[index]] = json.dumps(value)
                p.mset(key_values)
                p.execute()


task_manager = TaskManager()


class BaseCallback(celery.Task):
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
        logger.exception(f"[celery任务:{self.name}执行失败] task_id:{task_id},args:{args},kwargs:{kwargs}")

    # 任务成功时执行
    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"[celery任务:{self.name}执行成功] task_id:{task_id},args:{args},kwargs:{kwargs}")

    # 任务重试时执行
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.info(f"[celery任务:{self.name}开始重试] task_id:{task_id},args:{args},kwargs:{kwargs}")


# test
@celery.task(name="example_task", base=BaseCallback)
def example_task(m, n):
    return m + n


def __test_task_manager():
    task_id1 = task_manager.apply_async(example_task, (1, 2))
    task_id2 = task_manager.apply_async(example_task, (2, "1"))
    # 启动celery worker: celery -A server.core.celery_app worker -l info
    print(task_id1, task_manager.get_task_status(task_id1))

    time.sleep(5)

    assert task_manager.get_task_status(task_id1) == "SUCCESS"
    assert task_manager.get_task_status([task_id1, task_id2]) == {task_id1: "SUCCESS", task_id2: "FAILURE"}

    assert task_manager.get_task_result(task_id1) == 3
    assert (
        str(task_manager.get_task_result([task_id1, task_id2])[task_id2])
        == "unsupported operand type(s) for +: 'int' and 'str'"
    )


if __name__ == "__main__":
    __test_task_manager()
