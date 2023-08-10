import typing
from collections import OrderedDict

from core.logger import logger
from core.prometheus.Writer import SimpleRemoteWriter
from core.settings import settings
from core.utils.common import split_list


class PushLibrary(object):
    """推送通道工厂"""

    pcs = OrderedDict()

    @classmethod
    def register(cls, p_code, p_class):
        """注册组件"""
        if p_code and p_code not in cls.pcs:
            cls.pcs[p_code] = p_class

    @classmethod
    def get_pusher(cls, p_code):
        """获取组件类"""
        mc_class = cls.pcs.get(p_code)
        if mc_class is None:
            raise Exception("pusher %s does not exist." % p_code)
        return mc_class


class MetaPusher(type):
    def __new__(cls, name, bases, attrs):
        p_class = super().__new__(cls, name, bases, attrs)
        p_code = attrs.get("code")
        PushLibrary.register(p_code, p_class)
        return p_class


class Pusher(metaclass=MetaPusher):
    code = ""

    async def _push(self, data):
        pass

    async def push(self, data):
        format_data = self.format(data)
        if self.validate(format_data):
            await self._push(format_data)

    async def mpush(self, data: typing.Iterable):
        for _data in data:
            await self.push(data)

    async def validate(self, data) -> bool:
        return True

    async def format(self, data):
        return data


class PrometheusPusher(Pusher):
    code = "prometheus"

    def __init__(
        self,
        rw_url=settings.prometheus_rw_url,
        user=settings.prometheus_user,
        password=settings.prometheus_pwd,
        max_length=100,
    ):
        self.rw_url = rw_url
        self.user = user
        self.password = password
        self.max_length = max_length
        self.client = SimpleRemoteWriter(self.rw_url, self.user, self.password)

    async def _push(self, data):
        await self.client.write(*data)

    async def mpush(self, data):
        validated_data = []
        for _data in data:
            fmt_data = self.format(_data)
            if self.validate(fmt_data):
                validated_data.append(_data)
        sublists = split_list(validated_data, self.max_length)
        count = 0
        for sublist in sublists:
            try:
                await self.client.writes(sublist)
                count += len(sublist)
            except Exception:
                logger.exception(f"prometheus push error,url:{self.rw_url}")
        return count

    def format(self, data):
        return data

    def validate(self, data) -> bool:
        # todo 校验时间差距不得超过24小时
        return True


# 使用同一对象,避免多次连接
prom_pusher = PushLibrary.get_pusher("prometheus")()
