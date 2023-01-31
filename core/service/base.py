import functools
import inspect
from collections import defaultdict

from pydantic.main import BaseModel

from core.driver.base import register_driver

PRE_RUN = "pre_run"
POST_RUN = "post_run"


def set_hook(fn, key, **kwargs):
    if fn is None:
        return functools.partial(set_hook, key=key, **kwargs)
    try:
        hook_config = fn.__hook__
    except AttributeError:
        fn.__hook__ = hook_config = {}
    hook_config[key] = kwargs
    return fn


def pre_run(fn=None):
    return set_hook(fn, PRE_RUN)


def post_run(fn=None):
    return set_hook(fn, POST_RUN)


class ServiceMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        cls._hooks = mcs.resolve_hooks(cls)
        return cls

    @classmethod
    def resolve_hooks(mcs, cls):
        mro = inspect.getmro(cls)

        hooks = defaultdict(list)

        for attr_name in dir(cls):
            for parent in mro:
                try:
                    attr = parent.__dict__[attr_name]
                except KeyError:
                    continue
                else:
                    break
            else:
                continue

            try:
                hook_config = attr.__hook__
            except AttributeError:
                pass
            else:
                for key in hook_config.keys():
                    hooks[key].append(attr_name)

        return hooks


class BaseService(object, metaclass=ServiceMeta):
    pass


class DriverService(BaseService):
    __driver_tag__ = "base"
    driver_run_fn = "run"
    input_model = BaseModel
    output_model = BaseModel
    _error = None

    def __init__(self, input: input_model, driver_conf: dict = None):
        self.input = input or self.input_model()
        driver_conf = driver_conf or {}
        self.driver = self.get_driver(**driver_conf)
        self.output: BaseModel = self.output_model()

    def _has_hook(self, tag) -> bool:
        return bool(self._hooks[tag])

    def invoke_hook(self, tag):
        for proc_name in self._hooks[tag]:
            proc = getattr(self, proc_name)
            proc()

    def __call__(self):
        if self._has_hook(PRE_RUN):
            self.invoke_hook(PRE_RUN)
        self._run()
        if self._has_hook(POST_RUN):
            self.invoke_hook(POST_RUN)
        return self.output

    def _run(self):
        self.output = getattr(self.driver, self.driver_run_fn, "run")(**self.input.dict())

    @property
    def error(self):
        return self._error

    def get_driver(self, **kwargs):
        driver_class = register_driver.get(self.__driver_tag__)
        assert driver_class is not None, (
            f"{self.__class__.__name__} must set class attribute `__driver_tag__` or "
            f"implemented method `get_driver`  "
        )
        return driver_class(**kwargs)
