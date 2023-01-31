import json

import requests

from core.driver.base import Driver
from core.logger import logger

DEFAULT_HEADER = {"Content-Type": "application/vnd.yang.data+json", "Accept": "application/vnd.yang.data+json"}


class RestConf(Driver):
    __tag__ = "rest"

    def __init__(
        self,
        uri,
        host,
        port,
        username,
        password,
        transport=False,
        action=False,
        headers=None,
        payload=False,
        params=False,
        connection_args={},
    ):
        self.uri = uri
        self.connection_args = connection_args
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.headers = headers or DEFAULT_HEADER
        self.transport = transport
        self.action = action
        self.payload = payload
        self.params = params

    def send_command(self, session=False, command=False):
        try:
            result = {}
            url = self.transport + "://" + self.host + ":" + str(self.port) + self.uri
            response = requests.get(
                url,
                auth=(self.username, self.password),
                params=self.params,
                headers=self.headers,
                **self.connection_args
            )
            try:
                res = json.loads(response.text)
            except Exception:
                res = ""
                pass
            result[url] = {}
            result[url]["status_code"] = response.status_code
            result[url]["result"] = res
            return result
        except Exception as e:
            logger.error(e)

    def config(self, session=False, command=False):
        try:
            result = {}
            url = self.transport + "://" + self.host + ":" + str(self.port) + self.uri
            if hasattr(requests, str(self.action)):
                response = getattr(requests, str(self.action))(
                    url,
                    auth=(self.username, self.password),
                    data=json.dumps(self.payload),
                    params=self.params,
                    headers=self.headers,
                    **self.connection_args
                )
                try:
                    res = json.loads(response.text)
                except Exception:
                    res = ""
                    pass
                result[url] = {}
                result[url]["status_code"] = response.status_code
                result[url]["result"] = res
                return result
            else:
                raise Exception(self.action + " not found in requests")
        except Exception as e:
            logger.error(e)
