import unittest
import warnings

from core.driver.netmiko.credentials import Credentials
from core.driver.netmiko.netmiko_client import NetMikoClient


class NetMikoClientTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.client = NetMikoClient()
        self.credentials = Credentials(
            username="umr",
            password="umr",
        )

    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        super().setUpClass()

    def test_send_command(self):
        print(self.client.send_command("172.16.1.134", self.credentials, "cisco_ios", ["show ssh"], enable_mode=False))

    def test_send_config(self):
        print(
            self.client.send_config("172.16.1.134", self.credentials, "cisco_ios", ["snmp-server community public rw"])
        )

    def test_send_struct_output_command(self):
        print(self.client.send_struct_output_command("172.16.1.134", self.credentials, "cisco_ios", "show ip arp"))


if __name__ == "__main__":
    unittest.main()
