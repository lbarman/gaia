import sys
import unittest
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import gaia_client.system as system


class SystemTest(unittest.TestCase):

    def test_system_status(self):
        res = system.get_system_status()

        self.assertNotEqual(res, None)
        self.assertNotEqual(res['uptime'], None)
        self.assertNotEqual(res['free'], None)
        self.assertNotEqual(res['ps'], None)
        self.assertNotEqual(res['df'], None)


if __name__ == '__main__':
    unittest.main()
