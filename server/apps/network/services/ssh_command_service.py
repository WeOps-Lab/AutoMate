from core.driver.netmiko.credentials import Credentials
from core.driver.netmiko.entity.network_ssh_result import NetworkSshResult
from core.driver.netmiko.netmiko_client import NetMikoClient
from server.apps.network.forms.ssh_command import SshCommand


class SshCommandService:
    def __init__(
        self,
    ) -> None:
        super().__init__()

    def execute_ssh_command(self, data: SshCommand) -> NetworkSshResult:
        credentials = Credentials(username=data.username, password=data.password, enable=data.secret or data.password)
        client = NetMikoClient()
        return client.send_command(
            ip=data.host,
            device_type=data.device_type,
            commands=data.commands,
            credentials=credentials,
            port=data.port,
            enable_mode=data.enable_mode,
            timeout=data.timeout,
        )
