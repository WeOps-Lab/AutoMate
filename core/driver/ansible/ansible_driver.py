import os
import time
import uuid

from core.driver.ansible.constansts import DEFAULT_HANDLER, PROMETHEUS_HANDLER
from core.driver.ansible.form.adhoc_result import AdHocResult
from core.driver.ansible.handlers.base import register_handlers, runner_handlers
from core.driver.base import Driver
from core.logger import logger
from core.settings import settings

try:
    import ansible_runner
except Exception:
    logger.warning("无法加载Ansible Runner模块,ADHoc部分功能可能无法正常工作")


class AnsibleDriver(Driver):
    __tag__ = "ansible"

    def run_playbook(self, playbook_name: str, extra_vars: dict = None):
        """
        :param playbook_name: 文件路径asserts/playbooks/{playbook_name}/main.py
        :param extra_vars: 额外变量,可用{{ key }} ,例如 extra_vars = {key:xx}
        :return: AdHocResult
        """
        rc = ansible_runner.RunnerConfig(
            settings.private_data_path,
            playbook=f"{settings.playbook_path}/{playbook_name}/main.yml",
            inventory=settings.inventory_path,
            extravars=extra_vars or {},
        )
        rc.prepare()
        _uuid = str(uuid.uuid1())
        runner = ansible_runner.Runner(config=rc)
        runner.run()
        runner._uuid = _uuid
        result: AdHocResult = self.get_result(runner)  # noqa
        return result

    def build_inventory(self, inventories):
        """
        172.16.60.220 ansible_ssh_user=root ansible_ssh_pass=123456 ansible_ssh_port=22
        172.16.60.221 ansible_ssh_user=root ansible_ssh_pass=bo@123 ansible_ssh_port=22
        172.16.60.222 ansible_ssh_user=app ansible_ssh_pass=bj@123 ansible_ssh_port=22 ansible_sudo_pass=bj@123
        """
        inventory_format = "{host} ansible_ssh_user={user} ansible_ssh_pass={password} ansible_ssh_port={port}"
        inventory_list = []
        for inventory in inventories:
            host = inventory.host
            if not host:
                continue
            user = inventory.user or "root"
            password = inventory.password or ""
            port = inventory.port or 22
            inventory_str = inventory_format.format(host=host, user=user, password=password, port=port)
            inventory_list.append(inventory_str)
        return "\n".join(inventory_list)

    def run_adhoc(
        self,
        module_name: str,
        module_args: str = "",
        is_async=False,
        timeout=None,
        extravars: dict = None,
        inventory=None,
        **kwargs,
    ) -> AdHocResult:
        """

        :param module_name: 模块名,可内置,可ansible_plugins.modules下 ,即-m
        :param module_args: 模块参数,即-a "xx"
        :param is_async: 是否异步,默认同步
        :param timeout: 是否设置超时,如执行超时则status = "timeout"
        :param kwargs: 其他run参数,如finished_callback等,可查看ansible_runner/interface run
        :return: AdHocResult
        """
        # 异步场景下添加uuid记录
        _uuid = str(uuid.uuid1())
        kwargs = self.load_handler(**kwargs)
        is_local = True
        temporary_inventory_file = ""
        if inventory:
            now = int(time.time())
            file_name = f"temporary_inventory_{now}"
            temporary_inventory_file = os.path.join(settings.base_dir, file_name)
            inventory_str = self.build_inventory(inventory)
            if inventory_str:
                with open(temporary_inventory_file, "w") as f:
                    f.write(inventory_str)
                is_local = False
        if is_async and is_local:
            if "finished_callback" not in kwargs:
                kwargs.update(finished_callback=register_handlers[DEFAULT_HANDLER])

            _thread, runner = ansible_runner.run_async(
                host_pattern="localhost",
                module=module_name,
                module_args=module_args,
                json_mode=True,
                timeout=timeout,
                extravars=extravars or {},
                **kwargs,
            )
            logger.info(f"start thread to run ansible work ,module_name:{module_name},module_args:{module_args}")
        elif is_async and not is_local:
            if "finished_callback" not in kwargs:
                kwargs.update(finished_callback=register_handlers[DEFAULT_HANDLER])

            _thread, runner = ansible_runner.run_async(
                host_pattern="*",
                inventory=temporary_inventory_file,
                module=module_name,
                module_args=module_args,
                json_mode=True,
                timeout=timeout,
                extravars=extravars or {},
                **kwargs,
            )
            logger.info(f"start thread to run ansible work ,module_name:{module_name},module_args:{module_args}")
        elif not is_async and not is_local:
            runner = ansible_runner.run(
                host_pattern="*",
                inventory=temporary_inventory_file,
                module=module_name,
                module_args=module_args,
                json_mode=True,
                timeout=timeout,
                extravars=extravars or {},
                **kwargs,
            )
            os.remove(temporary_inventory_file)
        else:
            runner = ansible_runner.run(
                host_pattern="localhost",
                module=module_name,
                module_args=module_args,
                json_mode=True,
                timeout=timeout,
                extravars=extravars or {},
                **kwargs,
            )

        runner._uuid = _uuid
        runner.temporary_inventory_file = temporary_inventory_file
        result: AdHocResult = self.get_result(runner, is_async=is_async)
        return result

    def run_adhoc_to_prometheus(self, module_name: str, module_args: str = "", **kwargs):
        self.run_adhoc(module_name, module_args, finished_callback=PROMETHEUS_HANDLER, **kwargs)

    def async_run_adhoc(self, module_name: str, module_args: str = "", **kwargs):
        self.run_adhoc(module_name, module_args, is_async=True, **kwargs)

    def get_result(self, runner, is_async=False) -> AdHocResult:
        timeout = runner.config.timeout
        result = {}
        message = ""
        success = True
        if is_async:
            message = "async run ansible command"
        else:
            for e in runner.events:
                if e["event"] == "runner_on_ok":
                    result = e["event_data"]["res"]
                    break
                elif e["event"] == "runner_on_failed":
                    message = str(e["event_data"]["res"].get("msg", "ansible执行失败"))
                    success = False
                    break
                elif e["event"] == "runner_on_unreachable":
                    message = str(e["event_data"]["res"].get("msg", "ansible主机无法链接"))
                    success = False
                    break
            else:
                if timeout:
                    message = f"failed: runner timeout [timeout:{timeout}],please check kwargs `timeout` value "
                else:
                    message = "failed: runner unknown error "
                success = False
        result = result or {}
        result.update(uuid=runner._uuid)
        return AdHocResult(result=result, message=message, success=success)

    def load_handler(self, **kwargs):
        for handler, handler_name in kwargs.items():
            if handler in runner_handlers and isinstance(handler_name, str) and handler_name in register_handlers:
                kwargs[handler] = register_handlers[handler_name]
        return kwargs


ansible_driver = AnsibleDriver()
