import builtins
import importlib

# pipeline mako render settings
MAKO_SANDBOX_SHIELD_WORDS = [
    "ascii",
    "bytearray",
    "bytes",
    "callable",
    "chr",
    "classmethod",
    "compile",
    "delattr",
    "dir",
    "divmod",
    "exec",
    "eval",
    "filter",
    "frozenset",
    "getattr",
    "globals",
    "hasattr",
    "hash",
    "help",
    "id",
    "input",
    "isinstance",
    "issubclass",
    "iter",
    "locals",
    "map",
    "memoryview",
    "next",
    "object",
    "open",
    "print",
    "property",
    "repr",
    "setattr",
    "staticmethod",
    "super",
    "type",
    "vars",
    "__import__",
]

# format: module_path: alias
MAKO_SANDBOX_IMPORT_MODULES = {
    "datetime": "datetime",
    "re": "re",
    "hashlib": "hashlib",
    "random": "random",
    "time": "time",
    "os.path": "os.path",
}

SANDBOX = {}


class MockStrMeta(type):
    def __new__(cls, name, bases, attrs):
        new_cls = super(MockStrMeta, cls).__new__(cls, name, bases, attrs)
        SANDBOX.update({new_cls.str_return: new_cls})
        return new_cls

    def __str__(cls):
        return cls.str_return

    def __call__(cls, *args, **kwargs):
        return cls.call(*args, **kwargs)


def _shield_words(sandbox, words):
    for shield_word in words:
        sandbox[shield_word] = None


class ModuleObject:
    def __init__(self, sub_paths, module):
        if len(sub_paths) == 1:
            setattr(self, sub_paths[0], module)
            return
        setattr(self, sub_paths[0], ModuleObject(sub_paths[1:], module))


def _import_modules(sandbox, modules):
    for mod_path, alias in modules.items():
        mod = importlib.import_module(mod_path)
        sub_paths = alias.split(".")
        if len(sub_paths) == 1:
            sandbox[alias] = mod
        else:
            sandbox[sub_paths[0]] = ModuleObject(sub_paths[1:], mod)


def _mock_builtins():
    """
    @summary: generate mock class of built-in functions like id,int
    """
    for func_name in dir(builtins):
        if func_name.lower() == func_name and not func_name.startswith("_"):
            new_func_name = "Mock{}".format(func_name.capitalize())
            MockStrMeta(new_func_name, (object,), {"call": getattr(builtins, func_name), "str_return": func_name})


_mock_builtins()

_shield_words(SANDBOX, MAKO_SANDBOX_SHIELD_WORDS)

_import_modules(SANDBOX, MAKO_SANDBOX_IMPORT_MODULES)
