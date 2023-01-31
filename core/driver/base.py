from collections import OrderedDict

register_driver = OrderedDict()


class MetaDriver(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(MetaDriver, cls).__new__(cls, name, bases, attrs)
        _tag = attrs.get("__tag__")
        assert _tag is not None, f"register driver:{name} must set class property `__tag__`  "
        register_driver.update({_tag: new_class})
        return new_class


class Driver(metaclass=MetaDriver):
    __tag__ = "base"

    def run(self, *args, **kwargs):
        pass
