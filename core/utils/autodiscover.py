import importlib


class AutoDiscover:
    """
    This class search modules from a given path recursively.
    It searches all the modules and run an `import_module` for each.
    :param path: `pathlib.Path` object
    :param pattern: str object - (Optional)
    :return: None
    How to use:
        autodiscover = AutoDiscover(path="path/to/models", pattern="model")
        autodiscover()
    """

    def __init__(self, path, pattern=None):
        self.path = path
        self.pattern = pattern

    def __call__(self):
        return self.__execute(path=self.path, pattern=self.pattern)

    def __execute(self, path, pattern):
        modules = [_ for _ in self.__get_modules_from(path)]

        for module in reversed(modules):
            if module.name.startswith("_"):
                continue

            if module.is_file() and module.match(pattern or "*"):
                module_name = self.__normalize_module_name(module)

                importlib.import_module(module_name)

    def __get_modules_from(self, path):
        return list(path.glob("**/*.py"))

    def __normalize_module_name(self, module):
        return ".".join(module.parts).replace(".py", "")
