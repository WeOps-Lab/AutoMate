from puresnmp import puresnmp

from core.driver.base import Driver
from core.logger import logger


class PureSNMPClient(Driver):
    __tag__ = "puresnmp"

    def __init__(self, port=161, timeout=2, action_type="get"):
        self.port = port
        self.timeout = timeout
        self.action_type = action_type

    def send_command(self, ip, community, session=False, command=None):
        try:
            command = command or []
            result = {}
            for c in command:
                # remove timeout weirdness for tables
                if self.action_type == "table":
                    response = getattr(puresnmp, self.action_type)(ip=ip, community=community, oid=c, port=self.port)
                else:
                    response = getattr(puresnmp, self.action_type)(
                        ip=ip,
                        community=community,
                        oid=c,
                        port=self.port,
                        timeout=self.timeout,
                    )

                # remnder result data for get call
                if self.action_type == "get":
                    if isinstance(response, bytes):
                        response = response.decode(errors="ignore")
                    result[c] = response
                # remnder result data for walk call
                elif self.action_type == "walk":
                    result[c] = []
                    for row in response:
                        oid = str(row[0])
                        oid_raw = row[1]
                        if isinstance(oid_raw, bytes):
                            oid_raw = oid_raw.decode(errors="ignore")
                        result[c].append({oid: oid_raw})
                # remnder result data for table call
                elif self.action_type == "table":
                    result[c] = []
                    for key in response[0]:
                        oid = str(key)
                        oid_raw = response[0][key]
                        if isinstance(response[0][key], bytes):
                            oid_raw = oid_raw.decode(errors="ignore")
                        result[c].append({oid: oid_raw})
                else:
                    result[c] = f"{response}"
            return result
        except Exception as e:
            logger.error(e)
