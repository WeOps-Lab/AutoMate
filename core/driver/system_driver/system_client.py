import os
import subprocess

from core.driver.base import Driver
from core.logger import logger


class SystemClient(Driver):
    __tag__ = "system_cmd"

    @staticmethod
    def run(command: str):
        system_env = dict(os.environ)
        # system_env['ANSIBLE_LOAD_CALLBACK_PLUGINS'] = 'true'
        # system_env['ANSIBLE_STDOUT_CALLBACK'] = 'json'

        logger.info(f"执行命令{command}")
        proc = subprocess.Popen(
            command,
            env=system_env,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1,
        )
        out, err = proc.communicate()
        return out, err
