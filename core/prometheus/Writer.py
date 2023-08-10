import calendar

import aiohttp
import snappy

from .prometheus_pb2 import WriteRequest


def dt2ts(dt):
    """Converts a datetime object to UTC timestamp
    naive datetime will be considered UTC.
    """
    return calendar.timegm(dt.utctimetuple())


class RemoteWriter(object):
    def __init__(self, url, auth=None):
        super(RemoteWriter, self).__init__()
        self._url = url
        self._headers = {
            "Content-Encoding": "snappy",
            "Content-Type": "application/x-protobuf",
            "X-Prometheus-Remote-Write-Version": "0.1.0",
            "User-Agent": "metrics-worker",
        }
        self._auth = auth

    async def _pack(self, write_request, ts, name, labels, value):
        series = write_request.timeseries.add()

        label = series.labels.add()
        label.name = "__name__"
        label.value = name

        for k, v in labels.items():
            label = series.labels.add()
            label.name = k
            label.value = v

        sample = series.samples.add()
        sample.value = value
        sample.timestamp = ts

    async def _send(self, write_request):
        uncompressed = write_request.SerializeToString()
        compressed = snappy.compress(uncompressed)

        try:
            async with aiohttp.ClientSession() as session:
                response = await session.post(self._url, headers=self._headers, auth=self._auth, data=compressed)
                if not response.ok:
                    response.raise_for_status()
        except aiohttp.ClientError as err:
            raise err
        return response

    async def write(self, ts, name, labels, value):
        write_request = WriteRequest()
        await self._pack(write_request, ts, name, labels, value)

        await self._send(write_request)

    async def writes(self, lines):
        write_request = WriteRequest()
        for line in lines:
            await self._pack(write_request, line[0], line[1], line[2], line[3])

        await self._send(write_request)


class SimpleRemoteWriter(RemoteWriter):
    def __init__(self, url, user=None, passwd=None):
        auth = None
        if all([user, passwd]):
            auth = aiohttp.BasicAuth(user, passwd)

        super(SimpleRemoteWriter, self).__init__(url, auth=auth)
