import json
from collections import OrderedDict

from core.db.redis_client import redis_client
from core.driver.ansible import constansts as c

runner_handlers = {
    "event_handler",
    "status_handler",
    "artifacts_handler",
    "cancel_callback",
    "finished_callback",
}
register_handlers = OrderedDict()


class BaseMetaHandler(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(BaseMetaHandler, cls).__new__(cls, name, bases, attrs)
        for i in attrs:
            if i in runner_handlers:
                register_handlers.update({f"{name}.{i}": getattr(new_class, i)})
        return new_class


class BaseHandler(metaclass=BaseMetaHandler):
    @classmethod
    def finished_callback(cls, runner):
        timeout = runner.config.timeout or c.DEFAULT_ANSIBLE_RUNNER_MAX_TIMEOUT
        redis_client.set(c.ANSIBLE_RUNNER_KEY.format(runner._uuid), json.dumps({"status": runner.status}), ex=timeout)
