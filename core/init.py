import logging
import os
import pathlib

from core.driver.ansible.credential import ModuleCredentialLibrary
from core.logger import logger
from core.logger.conf import LOGGER_NAMES, LOGURU_CONFIG
from core.logger.handlers import InterceptHandler
from core.settings import settings
from core.utils.autodiscover import AutoDiscover


class InitService(object):
    _init = False

    def __call__(self, *args, **kwargs):
        if not self.__class__._init:
            # 把自定义模块写入到环境变量中,方便模块寻找
            os.environ["ANSIBLE_LIBRARY"] = settings.ansible_library
            os.environ["ANSIBLE_MODULE_UTILS"] = settings.ansible_module_utils
            _register_driver()
            _register_ansible_handler()
            _init_credentials()
            _init_format()
            _init_logger()
            self.__class__._init = True


def _register_driver():
    AutoDiscover(pathlib.Path(settings.driver_path))()


def _register_ansible_handler():
    AutoDiscover(pathlib.Path(settings.ansible_handler_path))()


def _init_credentials():
    AutoDiscover(pathlib.Path(settings.server_path), "credential.py")()
    AutoDiscover(pathlib.Path(settings.server_path), "credential/*.py")()
    ModuleCredentialLibrary.init_mc()


def _init_format():
    AutoDiscover(pathlib.Path(settings.server_path), "format/*.py")()
    AutoDiscover(pathlib.Path(settings.server_path), "format.py")()


def _init_logger():
    for logger_name in LOGGER_NAMES:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
    logger.configure(**LOGURU_CONFIG)


init_service = InitService()
