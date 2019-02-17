import sys
import unittest
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import gaia_client.system as system


class SystemTest(unittest.TestCase):

    def test_system_status(self):

        s = system.System()
        res = s.get_system_status()

        self.assertNotEqual(res, None)
        self.assertNotEqual(res['uptime'], None)
        self.assertNotEqual(res['memory'], None)
        self.assertNotEqual(res['processes'], None)
        self.assertNotEqual(res['disk_usage'], None)

    def test_mock_system_status(self):

        s = system.MockSystem()
        res = s.get_system_status()

        self.assertNotEqual(res, None)
        self.assertNotEqual(res['uptime'], None)
        self.assertNotEqual(res['memory'], None)
        self.assertNotEqual(res['processes'], None)
        self.assertNotEqual(res['disk_usage'], None)

    def test_mock_shutdown(self):

        s = system.MockSystem()
        s.shutdown()
        self.assertTrue(s.shutdown_called)

    def test_mock_reboot(self):

        s = system.MockSystem()
        s.reboot()
        self.assertTrue(s.reboot_called)


if __name__ == '__main__':
    unittest.main()
