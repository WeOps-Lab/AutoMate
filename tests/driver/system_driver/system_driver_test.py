import unittest
import warnings


class SystemClientTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        super().setUpClass()


if __name__ == "__main__":
    unittest.main()
