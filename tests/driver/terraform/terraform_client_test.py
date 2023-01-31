import unittest
import warnings

from core.driver.terraform.terraform_client import TerraformClient


class TerraformClientTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        super().setUpClass()

    def test_terraform_client(self):
        client = TerraformClient(workspace="./asserts/working_test", folder_path="./working_test")
        return_code, stdout, stderr = client.apply()
        print(stderr)
        print(stdout)
        self.assertEqual(return_code, 0)
        self.assertIn("Apply complete!", stdout.replace('"', ""))
        self.assertIn("test = not_set", stdout.replace('"', ""))
        self.assertEqual(stderr.replace('"', ""), "")


if __name__ == "__main__":
    unittest.main()
