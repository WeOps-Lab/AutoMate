import unittest

from core.driver.jvm.jvm_runner import JvmRunner


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_run_sample(self):
        print(JvmRunner.run_sample())


if __name__ == "__main__":
    unittest.main()
