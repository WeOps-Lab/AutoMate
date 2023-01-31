import unittest
import warnings

from core.driver.ansible.ansible_driver import AnsibleDriver


class AnsibleRunnerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        super().setUpClass()

    def test_run(self):
        runner = AnsibleDriver()
        result = runner.run_local_adhoc(module_name="ping", module_args="")
        print(result)

    def test_run_ad(self):
        runner = AnsibleDriver()
        result = runner.run_local_adhoc(module_name="update_password", module_args="")
        print(result)


if __name__ == "__main__":
    unittest.main()
