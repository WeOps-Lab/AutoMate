from collections import OrderedDict

from core.exception.base import FormatError
from core.logger import logger
from core.utils.mako_utils import ConstantTemplate, to_mako_repr

KEY_METHOD_PREFIX = "get_"


class FormatLibrary(object):
    formats = OrderedDict()

    @classmethod
    def get_format_class(cls, code):
        return cls.formats.get(code)

    @classmethod
    def get_format(cls, code, data, context=None):
        code = code.lower()
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
        # 收集已重写get_key方法的key
        new_class._get_implement_keys(bases, attrs)

        new_class._build_tmp()
        FormatLibrary.formats[new_class.code] = new_class
        return new_class


def build_keys(d, keys=None, key_prefix="", val_prefix=KEY_METHOD_PREFIX):
    # 支持多级重写
    keys = keys or []
    for k, v in d.items():
        if isinstance(v, dict):
            keys += build_keys(v, key_prefix=f"{k}.", val_prefix=f"{val_prefix}{k}_")
            continue
        if not key_prefix:
            keys.append((f"{k}", f"{val_prefix}{k}"))
        else:
            keys.append((f"{key_prefix}{k}", f"{val_prefix}{k}"))
    return keys


class Format(metaclass=FormatMeta):
    code = ""
    format_map = {}

    def __init__(self, value, context=None):
        self.value = value
        self.context = context or {}

    @property
    def is_list(self):
        return isinstance(self.value, list)

    @property
    def is_ldict(self):
        return isinstance(self.value, dict) and all(map(lambda x: isinstance(x, list), self.value.values()))

    def get_format_map(self):
        return self.format_map

    def _get_item(self, item):
        return item

    def _get(self):
        if not self.format_map:
            return self.value
        return self._get_impl(self.value)

    def get(self):
        result = self._get()
        return result

    def _get_impl(self, item, *args, **kwargs):
        result = {}
        for i, method in self._implement_keys.items():
            result.update({i: method(self, item, context=self.context)})
        return result

    @classmethod
    def _get_implement_keys(cls, bases, attrs):

        implement_keys = []
        if "format_map" in attrs:
            implement_keys = [(key, attrs[value]) for key, value in build_keys(attrs["format_map"]) if value in attrs]

        # Ensures a base class field doesn't override cls attrs, and maintains
        # field precedence when inheriting multiple parents. e.g. if there is a
        # class C(A, B), and A and B both define 'field', use 'field' from A.
        known = set(attrs)

        def visit(name):
            known.add(name)
            return name

        base_implement_keys = [
            (visit(name), f)
            for base in bases
            if hasattr(base, "_implement_keys")
            for name, f in base._implement_keys.items()
            if name not in known
        ]
        cls._implement_keys = OrderedDict(implement_keys + base_implement_keys)

    @classmethod
    def _build_tmp(cls):
        pass


class MakoFormat(Format):
    code = "mako"
    format_map = {}

    @classmethod
    def _build_tmp(cls):
        cls.format_map = to_mako_repr(cls.format_map)
        tmp = {}
        tmp["root"] = ConstantTemplate(cls.format_map)
        if all(map(lambda x: isinstance(x, dict), cls.format_map.values())):
            for sub, fmt in cls.format_map.items():
                tmp[sub] = ConstantTemplate(fmt)
        cls._tmp = tmp

    def _get(self):
        if self.is_list:
            result = []
            for item in self.value:
                item_value = {**item, **self.context}
                item_result = self._resolve(item_value)
                item_result.update(self._get_impl(item_value))
                result.append(item_result)
        elif self.is_ldict:
            result = {}
            for k, v in self.value.items():
                for v_item in v:
                    v_item_value = {**v_item, **self.context}
                    v_item_result = self._resolve(v_item_value, key=k)
                    v_item_result.update(self._get_impl(v_item_value, pre_key=f"{k}."))
                    result.setdefault(k, []).append(v_item_result)
        else:
            value = {**self.value, **self.context}
            result = self._resolve(value)
            result.update(self._get_impl(value))
        return result

    def _get_impl(self, item, *args, pre_key="", **kwargs):
        result = {}
        for i, method in self._implement_keys.items():
            if i.startswith(pre_key):
                key = i[len(pre_key) :]
                result.update({key: method(self, item, context=self.context)})
        return result

    def _resolve(self, value, key="root"):
        if key not in self.__class__._tmp:
            logger.warning(
                f"value key:`{key}` and format_map key unmatched  must in `{list(self.__class__._tmp.keys())}`"
            )
            raise Exception(f"resolve error value:{value},key:{key}")
        return self.__class__._tmp[key].resolve_data(value)


# class CredentialFormat(MakoFormat):
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


class CollectFormat(MakoFormat):
    code = "driver_collect"
    type = "base.collect"
    tag = "driver.collect"
    name = "采集数据转换(base)"
    desc = "采集数据转换(base)"
    format_map = {}
    assoc_key = ""  # 唯一值

    def get_assoc_key(self):
        return self.assoc_key

    def _get(self):
        if self.is_list:
            result = []
            for item in self.value:
                item_value = {**item, **self.context}
                item_result = self._resolve(item_value)
                item_result.update(self._get_impl(item_value))
                result.append(item_result)
        elif self.is_ldict:
            result = []
            for k, v in self.value.items():
                obj_map = {}
                for v_item in v:
                    v_item_value = {**v_item, **self.context}
                    v_item_result = self._resolve(v_item_value, key=k)
                    v_item_result.update(self._get_impl(v_item_value, pre_key=f"{k}."))
                    if "bk_inst_name" in v_item_result:
                        obj_map.update({v_item_result[self.get_assoc_key()]: v_item_result["bk_inst_name"]})
                        v_item_result.update(bk_obj_id=k)
                        result.append(v_item_result)
                self.context.update({f"{k}_map": obj_map})
        else:
            value = {**self.value, **self.context}
            result = self._resolve(value)
            result.update(self._get_impl(value))
        return result


class UniqueFormat(MakoFormat):
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
    可直接调用format_{type}  如format_cmp_collect,format_cmp_credential
    """

    def __getattr__(self, item: str):
        if item.startswith("format_"):
            type = item.replace("format_", "")

            format_adapt = FormatAdapt(type)
            return format_adapt
        raise FormatError(f"Format Error: attribute not exist , type:{item} invalid")


format_util = FormatUtil()
