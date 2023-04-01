import unittest

from src import pycngal


class TestPyCNGAL(unittest.TestCase):
    def test_request_swagger(self):
        self.assertEqual(
            True, True if pycngal.request_swagger() is not None else False
        )

    def test_request_data_summary(self):
        self.assertEqual(
            True, True if pycngal.request_data_summary() is not None else False
        )


if __name__ == "__main__":
    unittest.main()
