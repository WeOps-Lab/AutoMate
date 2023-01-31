from collections import OrderedDict

from core.exception.base import FormatError
from core.utils.clean_items import clean_items


class FormatLibrary(object):
    formats = OrderedDict()

    @classmethod
    def get_format_class(cls, code):
        return cls.formats.get(code)

    @classmethod
    def get_format(cls, code, data, context=None):
        if code not in cls.formats:
            raise FormatError(f"Format Error: code:{code} invalid")
        if not context:
            return cls.formats[code](data)
        return cls.formats[code](data, context)

    @classmethod
    def get_type_format(cls, type, key, data, context=None):
        code = f"{type}_{key}"
        return cls.get_format(code, data, context=context)


class FormatMeta(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(FormatMeta, cls).__new__

        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, FormatMeta)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class
        new_class = super_new(cls, name, bases, attrs)
        if not new_class.code:
            raise FormatError(f"Format Error : {new_class.__name__} code can't be empty.")

        FormatLibrary.formats[new_class.code] = new_class
        return new_class


class Format(metaclass=FormatMeta):
    code = ""
    format_map = {}

    def __init__(self, value, context=None):
        self.value = value
        self.context = context

    def get_format_map(self):
        return self.format_map

    def get(self):
        pass


class CredentialFormat(Format):
    code = "driver_credential"
    type = "base.credential"
    tag = "driver.credential"
    name = "凭据数据转换(base)"
    desc = "凭据数据转换(base)"
    format_map = {}

    def get(self):
        format_result = {}
        for module_arg, secret_key in self.get_format_map().items():
            secret_value = self.value.get(secret_key) or self.context.get(secret_key)
            format_result[module_arg] = secret_value
        return format_result


class CollectFormat(Format):
    code = "driver_collect"
    type = "base.collect"
    tag = "driver.collect"
    name = "采集数据转换(base)"
    desc = "采集数据转换(base)"
    format_map = {}

    def get(self):
        format_map = self.get_format_map()
        format_result = clean_items(self.value, format_map, context=self.context)
        return format_result


class UniqueFormat(Format):
    code = "driver_unique"
    type = "base"
    tag = "driver.unique"
    name = "唯一数据转换(base)"
    desc = "唯一数据转换(base)"
    unique_keys = []

    def get(self):
        return self.unique_keys


class FormatAdapt:
    def __init__(self, format_type):
        self.format_type = format_type

    def __call__(self, *args, **kwargs):
        return FormatLibrary.get_type_format(self.format_type, *args, **kwargs).get()


class FormatUtil:
    """
    可直接调用format_{type}  如format_ansible_collect,format_ansible_credential
    """

    def __getattr__(self, item: str):
        if item.startswith("format_"):
            type = item.replace("format_", "")

            format_adapt = FormatAdapt(type)
            return format_adapt
        raise FormatError(f"Format Error: attribute not exist , type:{item} invalid")


format_util = FormatUtil()
