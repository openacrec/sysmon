import unittest

import sysmon_client.main as main


class JsonStructure(unittest.TestCase):

    def test_something(self):
        self.assertEqual(main.GPU_EXISTS, True)


if __name__ == '__main__':
    unittest.main()
