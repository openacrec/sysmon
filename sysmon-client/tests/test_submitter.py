import unittest

from requests.exceptions import ConnectionError

from sysmon_client import submitter


class TestSubmitter(unittest.TestCase):
    """Tests for the submitter submodule."""

    def test_connect_error(self):
        """Check if the right error gets raised with no reachable server."""
        name = "UnitTester"
        address = "https://localhost:4000/post"
        with self.assertRaises(ConnectionError):
            submitter.submit(name, address)

    def test_connect_error_handling(self):
        """Check that no another exception occurs."""
        name = "UnitTester"
        address = "https://localhost:4000/post"
        try:
            submitter.submit(name, address)
        except ConnectionError:
            pass


if __name__ == '__main__':
    unittest.main()
