import jpype

from core.driver.base import Driver


class JvmRunner(Driver):
    __tag__ = "jvm"

    @staticmethod
    def run():
        jpype.startJVM()
        jpype.addClassPath("jars/umr.jar")
        test = jpype.JClass("org.megalab.Test")
        t = test()
        res = t.run_adhoc("hello world")
        return res
