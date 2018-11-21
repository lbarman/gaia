import urllib3
import unittest
from constants import *
from server_web import webserver
from time import sleep
from multiprocessing import Process


def run_flask():
    webserver.debug = False
    webserver.run(host='127.0.0.1', port=WEB_SERVER_PORT)


class MyTest(unittest.TestCase):

    def setUp(self):
        self.thread = Process(target=run_flask)
        self.thread.start()

        sleep(2)

        self.server_url = 'http://127.0.0.1:' + str(WEB_SERVER_PORT)
        self.http = urllib3.PoolManager(1)

    def test_server_is_up_and_running(self):
        r = self.http.request('GET', self.server_url, timeout=1.0)
        self.assertEqual(r.status, 200)
        self.http.clear()

    def test_asset_css(self):
        r = self.http.request('GET', self.server_url+"/public/css/gaia.css", timeout=1.0)
        self.assertEqual(r.status, 200)
        self.http.clear()

    def test_asset_js(self):
        r = self.http.request('GET', self.server_url+"/public/css/gaia.jpg", timeout=1.0)
        self.assertEqual(r.status, 200)
        self.http.clear()

    def test_asset_img(self):
        r = self.http.request('GET', self.server_url+"/public/css/jquery-3.3.1.min.js", timeout=1.0)
        self.assertEqual(r.status, 200)
        self.http.clear()

    def test_command_only_post(self):
        data = {}
        r = self.http.request('GET', self.server_url + "/command", fields=data, timeout=1.0)
        self.assertEqual(r.status, 404)
        self.http.clear()

    def test_command_no_pwd(self):
        data = {}
        r = self.http.request('POST', self.server_url + "/command", fields=data, timeout=2.0)
        self.assertEqual(r.status, 401)
        self.http.clear()

    def test_command_no_data(self):
        data = {'passphrase': AUTHENTICATION_TOKEN}
        r = self.http.request('POST', self.server_url + "/command", fields=data, timeout=2.0)
        self.assertEqual(r.status, 406)
        self.http.clear()

    def tearDown(self):
        self.thread.terminate()


if __name__ == '__main__':
    unittest.main()
