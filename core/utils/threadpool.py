from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps

from core.db.redis_client import redis_client
from core.settings import settings


class ThreadPool(ThreadPoolExecutor):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def shutdown(self, *args, **kwargs):
        # 避免使用with触发shutdown导致全局线程池结束.
        pass

    def submit(*args, **kwargs):
        # 支持callback模式
        future = ThreadPoolExecutor.submit(*args, **kwargs)
        fn = kwargs.pop("fn", None) or args[1]
        call_backs = getattr(fn, "_callback", OrderedDict())
        for callback in call_backs.values():
            future.add_done_callback(callback)
        return future


# 全局线程池
thread_pool = ThreadPool(settings.max_thread_num)

THREAD_COUNT_KEY = "THREADPOOL_COUNT_{task_uuid}"  # {"all":10,"finish":1}


def add_callback(call_fn):
    """
    :param call_fn: callback函数
    :return:
    example:

        def A_callback(future):
            print(future.result())
            print("A_callback")

        def B_callback(future):
            print("B_callback")

        @add_callback(A_callback)
        @add_callback(B_callback)
        def task(task_id):
            pass

    """

    def outer(func):
        if not hasattr(func, "_callback"):
            func._callback = OrderedDict()
        func._callback[call_fn.__name__] = call_fn

        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            return result

        return inner

    return outer


def index_tag(func):
    """先进先出原则:索引标注器,把_index返回给result方便排序"""

    @wraps(func)
    def inner(*args, **kwargs):
        _index = kwargs.pop("_index", None)
        result = func(*args, **kwargs)
        if _index is not None:
            result = (_index, result)
        return result

    return inner


def get_fifo_result(result):
    """先进先出原则:根据_index排序并返回对应result
    params : tuple (_index, result)
    return : result
    """
    return [_result[1] for _result in sorted(result, key=lambda x: x[0])]


def thread_run_task(func, bulk_params, *args):
    """多线程执行任务"""
    data = []
    future_to_data = {thread_pool.submit(func, *args, **params) for index, params in bulk_params}
    for future in as_completed(future_to_data):
        data.append(future.result())
    return data


def fifo_thread_run_task(func, bulk_params, *args):
    """先进先出多线程执行任务"""
    data = []
    future_to_data = {
        thread_pool.submit(func, *args, _index=index, **params) for index, params in enumerate(bulk_params)
    }  # 记录顺序
    for future in as_completed(future_to_data):
        data.append(future.result())
    return get_fifo_result(data)


def count_tag(func):
    """统计装饰器"""

    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        task_uuid = kwargs.pop("_task_uuid", None)
        if not task_uuid:
            return result
        task_key = THREAD_COUNT_KEY.format(**{"task_uuid": task_uuid})
        redis_client.hincrby(task_key, "finish", 1)
        if result:
            redis_client.hincrby(task_key, "success", 1)
        return result

    return inner


def count_thread_run_task(task_uuid, func, bulk_params, *args):
    """(计数器版多线程执行任务)"""
    data = []
    task_key = THREAD_COUNT_KEY.format(**{"task_uuid": task_uuid})
    redis_client.hset(task_key, "all", len(bulk_params))
    func = count_tag(func)

    future_to_data = {thread_pool.submit(func, *args, _task_uuid=task_uuid, **params) for params in bulk_params}
    for future in as_completed(future_to_data):
        data.append(future.result())
    return data


def get_task_execute_percent(task_uuid):
    task_key = THREAD_COUNT_KEY.format(task_uuid)
    value = redis_client.hgetall(task_key)
    finish_count = value.get("finish", 0)
    all_count = value.get("all", 0)
    if not finish_count:
        return 0
    return all_count / finish_count


def decorator_except(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return {"result": True, "data": res, "message": ""}
        except Exception as err:
            return {"result": True, "data": None, "message": err}

    return inner


# class TreadPoolManager(object):
#     _instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if not cls._instance:
#             cls._instance = super().__new__(cls)
#         return cls._instance
#
#     def __init__(self, pools, workers):
#         # 最大的线程池
#         self.max_thread_pool = pools
#         # 最大worker
#         self.max_worker = workers
#         # 线程管理
#         self.thread_pools = OrderedDict()
#
#     def add_thread_pool(self, max_workers, *args, wait: bool = True, timeout=None, **kwargs):
#
#         _thread_pool = None
#         if not wait and self.allow_add_thread(max_workers):
#             raise Exception("thread_pool size limit ,not create new thread_pool")
#         ctime = time.time()
#         while not _thread_pool:
#             if self.allow_add_thread(max_workers):
#                 thread_pool = ThreadPool(max_workers, *args, manager=self, **kwargs)
#                 self.thread_pools[thread_pool] = max_workers
#                 _thread_pool = thread_pool
#             time.sleep(.25)
#             if timeout and (time.time() - ctime) > timeout:
#                 break
#         return _thread_pool
#
#     def allow_add_thread(self, worker):
#         if self.total_thread > self.max_thread_pool:
#             return False
#         if self.total_workers + worker > self.max_worker:
#             return False
#         return True
#
#     @property
#     def total_thread(self):
#         return len(self.thread_pools.keys())
#
#     @property
#     def total_workers(self):
#         return sum(self.thread_pools.values())
#
#     def pop_thread_pool(self, thread_pool):
#         self.thread_pools.pop(thread_pool)
#         del thread_pool
#
#     def shutdown(self, wait=True):
#         for thread_pool in self.thread_pools:
#             thread_pool.shutdown(wait=wait)
#
#
