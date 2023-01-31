import typing
from collections import OrderedDict

from core.driver.ansible.utils import parse_dict_to_args
from core.utils.common import underline2hump
from core.utils.vault import HvacManager

module_credential_mapping = {
    # "output": 'bind_user="{user}" bind_dn="{dn}" bind_pw="{password}"'  # args_mapping/output写其一
    # "module_name": {"args_mapping": {"module_args_1": "secret_key1",
    #                                   "module_args_2": "secret_key12",
    #                                   "module_args_3": "secret_key3"},
    #                 "output":'bind_user="{user}" bind_dn="{dn}" bind_pw="{password}"' # args_mapping/output写其一
    #                  },
}


class BaseModuleCredentialMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        _module = attrs.get("_module")
        ModuleCredentialLibrary.register_mc(_module, new_class)
        return new_class


class ModuleCredentialLibrary(object):
    """模块工厂"""

    mcs = OrderedDict()

    @classmethod
    def register_mc(cls, module, mc_class):
        """注册组件"""
        if module and module not in cls.mcs:
            cls.mcs[module] = mc_class

    @classmethod
    def get_mc_class(cls, module):
        """获取组件类"""
        mc_class = cls.mcs.get(module)
        if mc_class is None:
            raise Exception("modules_credentials %s does not exist." % module)
        return mc_class

    @classmethod
    def init_mc(cls):
        for module, module_dict in module_credential_mapping.items():
            cls.mcs[module] = type(
                f"{underline2hump(module)}ModuleCredential",
                (BaseModuleCredential,),
                {
                    "_module": module,
                    "_args_mapping": module_dict.get("args_mapping", {}),
                    "_output": module_dict.get("output", ""),
                },
            )


class BaseModuleCredential(metaclass=BaseModuleCredentialMeta):
    _module = ""
    _args_mapping = {}
    _output = ""

    def __init__(self, input, context=None):
        self.input = input
        self.context = context or {}

    def get_outputs(self) -> str:
        if self._output:
            return self._output.format(**self.input)
        return parse_dict_to_args(self.get_module_args())

    def get_module_args(self) -> typing.Dict:
        module_args = {}
        for module_arg, secret_key in self._args_mapping.items():
            secret_value = self.input.get(secret_key)
            module_args[module_arg] = secret_value
        return module_args


def get_module_outputs(module, input, context=None):
    """
    获取模块参数
    :param module: ansible模块名
    :param input: 输入,一般指秘钥字典
    :param context: 上下文参数
    :return:
    """
    mc = ModuleCredentialLibrary.get_mc_class(module)(input=input, context=context)
    return mc.get_outputs()


def get_module_args_by_path(module, path, context=None, **kwargs):
    """ """
    secret = HvacManager().read_secret(path)
    mc = ModuleCredentialLibrary.get_mc_class(module)(input=secret, context=context)
    return mc.get_module_args(**kwargs)


def get_outputs_by_path(module: str, path: str, context=None) -> str:
    """ """
    secret = HvacManager().read_secret(path)
    mc = ModuleCredentialLibrary.get_mc_class(module)(input=secret, context=context)
    return mc.get_outputs()
