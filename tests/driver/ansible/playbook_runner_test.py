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
        result = runner.run_playbook(playbook_name="test_mkdir")
        print(result)


if __name__ == "__main__":
    unittest.main()
