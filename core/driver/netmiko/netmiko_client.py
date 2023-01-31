import re
from socket import timeout
from typing import Optional, Sequence, Tuple

import netmiko

from core.driver.base import Driver
from core.driver.netmiko.constants import DEVICE_TYPE_BASE_PROMPT
from core.driver.netmiko.credentials import Credentials
from core.driver.netmiko.entity.network_ssh_result import NetworkSshResult
from core.driver.netmiko.parser import parse_output
from core.logger import logger


class NetMikoClient(Driver):
    __tag__ = "netmiko"

    def send_struct_output_command(
        self,
        ip: str,
        credentials: Credentials,
        device_type: str,
        command: str,
        port: int = 22,
        delay_factor: int = 1,
        verbose: bool = False,
    ) -> NetworkSshResult:
        ssh_result = self.send_command(ip, credentials, device_type, [command], port, delay_factor, verbose)
        struct_output = parse_output(platform=device_type, command=command, data=ssh_result.command_result[command])

        result = NetworkSshResult()
        result.command_result = struct_output
        result.err_message = ssh_result.err_message
        return result

    def send_command(
        self,
        ip: str,
        credentials: Credentials,
        device_type: str,
        commands: Sequence[str],
        port: int = 22,
        delay_factor: int = 1,
        verbose: bool = False,
        enable_mode: bool = False,
        expect_string: str = "",
        timeout: int = 600,
    ) -> NetworkSshResult:

        """
        Instantiate a netmiko wrapper instance, feed me an IP, Platform Type, Username, Password, any commands to run.
        :param ip: What IP are we connecting to?
        :param credentials: A naas.library.auth.Credentials object with the username/password/enable in it
        :param commands: List of the commands to issue to the device
        :param device_type: What Netmiko device type are we connecting to?
        :param port: What TCP Port are we connecting to?
        :param delay_factor: Netmiko delay factor, default of 1, higher is slower but more reliable on laggy links
        :param verbose: Turn on Netmiko verbose logging
        :param expect_string: Regular expression pattern to use for determining end of output.If left blank will
               default to being based on router prompt.
        :param timeout: exec timeout.
        :return: A Tuple of a dict of the results (if any) and a string describing the error (if any)
        """

        # Create device dict to pass netmiko
        netmiko_device = {
            "device_type": device_type,
            "ip": ip,
            "username": credentials.username,
            "password": credentials.password,
            "secret": credentials.enable,
            "port": port,
            # "ssh_config_file": "/app/naas/ssh_config",
            "allow_agent": False,
            "use_keys": False,
            "verbose": verbose,
            "timeout": timeout,
        }
        result = NetworkSshResult()

        try:
            with netmiko.ConnectHandler(**netmiko_device) as net_connect:
                if not expect_string:
                    device_name = re.escape(net_connect.base_prompt)
                    expect_string = DEVICE_TYPE_BASE_PROMPT[device_type].format(device_name)

                if enable_mode:
                    logger.info(f"设备{ip}进入Enable模式.......")
                    net_connect.enable()

                net_output = {}
                for command in commands:
                    net_output[command] = net_connect.send_command(
                        command, delay_factor=delay_factor, expect_string=expect_string
                    )

        except Exception as e:
            result.command_result = {}
            result.err_message = str(e)
            return result

        logger.info("%s:Netmiko executed successfully.", ip)

        result.command_result = net_output
        result.err_message = ""
        return result

    def send_config(
        self,
        ip: str,
        credentials: Credentials,
        device_type: str,
        commands: Sequence[str],
        port: int = 22,
        save_config: bool = False,
        commit: bool = False,
        delay_factor: int = 1,
        verbose: bool = False,
    ) -> Tuple[Optional[dict], Optional[str]]:

        """
        Instantiate a netmiko wrapper instance, feed me an IP, Platform Type, Username, Password, any commands to run.
        :param ip: What IP are we connecting to?
        :param credentials: A naas.library.auth.Credentials object with the username/password/enable in it
        :param commands: List of the commands to issue to the device
        :param device_type: What Netmiko device type are we connecting to?
        :param port: What TCP Port are we connecting to?
        :param save_config: Do you want to save this configuration upon insertion? Default: False, don't save the config
        :param commit: Do you want to commit this candidate configuration to the running config?  Default: False
        :param delay_factor: Netmiko delay factor, default of 1, higher is slower but more reliable on laggy links
        :param verbose: Turn on Netmiko verbose logging
        :return: A Tuple of a dict of the results (if any) and a string describing the error (if any)
        """

        # Create device dict to pass netmiko
        netmiko_device = {
            "device_type": device_type,
            "ip": ip,
            "username": credentials.username,
            "password": credentials.password,
            "secret": credentials.enable,
            "port": port,
            # "ssh_config_file": "/app/naas/ssh_config",
            "allow_agent": False,
            "use_keys": False,
            "verbose": verbose,
        }

        try:
            logger.info("%s:Establishing connection...", ip)
            with netmiko.ConnectHandler(**netmiko_device) as net_connect:
                net_output = {}
                logger.info("%s:Sending config_set: %s", ip, commands)
                net_output["config_set_output"] = net_connect.send_config_set(commands, delay_factor=delay_factor)

                if save_config:
                    try:
                        logger.info("%s: Saving configuration", ip)
                        net_connect.save_config()
                    except NotImplementedError:
                        logger.info(
                            "%s: This device_type (%s) does not support the save_config operation.", ip, device_type
                        )

                if commit:
                    try:
                        logger.info("%s: Committing configuration", ip)
                        net_connect.commit()
                    except AttributeError:
                        logger.info("%s: This device_type (%s) does not support the commit operation", ip, device_type)

        except (netmiko.NetMikoTimeoutException, timeout) as e:
            logger.info("%s:Netmiko timed out connecting to device: %s", ip, e)
            return None, str(e)
        except netmiko.NetMikoAuthenticationException as e:
            logger.info("%s:Netmiko authentication failure connecting to device: %s", ip, e)
            return None, str(e)
        except Exception as e:
            logger.info("%s:Netmiko cannot connect to device: %s", ip, e)
            return None, ("Unknown SSH error connecting to device {}: {}".format(ip, str(e)))

        logger.info("%s:Netmiko executed successfully.", ip)
        return net_output, None
