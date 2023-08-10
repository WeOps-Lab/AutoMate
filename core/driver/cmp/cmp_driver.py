from core.driver.base import Driver
from core.logger import cmp_logger as logger

try:
    from cmp.cloud_apis.resource_client import ResourceClient
except Exception:
    raise ModuleNotFoundError("must build cmp directory or pip install -r cmp/requirements.txt")


class CMPDriver(Driver):
    """cloud manager platform"""

    __tag__ = "cmp"

    def __init__(self, account, password, cloud_type, region=None, host="", **kwargs):
        self.account = account
        self.password = password
        self.region = region
        self.cloud_type = cloud_type
        self.host = host
        self.kwargs = kwargs

    def __getattr__(self, item):
        """云资源操作方法:如list_vm,list_dist"""
        if item in ["shape", "__len__"]:
            return
        client = ResourceClient(
            self.account, self.password, self.region, self.cloud_type, host=self.host, **self.kwargs
        ).cw
        method = getattr(client, item)
        if not method:
            raise AttributeError(f"Cloud:{self.cloud_type} not define method `{item}`")
        return method

    def run(self, mname, **kwargs):
        try:
            _method = getattr(self, mname)
        except Exception:
            logger.exception("CMP Driver Error")
            return {"result": False}
        result = _method(**kwargs)
        return result
