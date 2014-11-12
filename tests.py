import unittest
import urllib
from urllib2 import urlopen
APP_ARRD = "http://127.0.0.1:8080"


class TestListener(unittest.TestCase):

    def test_get(self):
        response = urlopen(APP_ARRD)
        self.assertEqual(response.read(), "OK")

    def test_get_msg(self):
        response = urlopen(APP_ARRD + '?msg="test_message"')
        self.assertEqual(response.read(), "OK")

    def test_get_msg_state(self):
        response = urlopen(APP_ARRD + '?msg="test_message"')
        self.assertEqual(response.getcode(), 200)

    def test_get_state(self):
        response = urlopen(APP_ARRD)
        self.assertEqual(response.getcode(), 200)

    def test_post(self):
        response = urlopen(APP_ARRD, urllib.urlencode({'msg': 'test message',
                                                       'token': '123'}))
        self.assertEqual(response.getcode(), 200)

    def test_post_msg(self):
        response = urlopen(APP_ARRD, urllib.urlencode({'msg': 'test message',
                                                       'token': '123'}))
        self.assertEqual(response.read(), 'OK')

    def test_multiple_tokens(self):
        response = urlopen(APP_ARRD, urllib.urlencode({'msg': 'test message',
                                                       'token': ['123', '55']}))
        self.assertEqual(response.getcode(), 200)

    def test_empty_post(self):
        response = urlopen(APP_ARRD, urllib.urlencode({}))
        self.assertEqual(response.getcode(), 200)

    
if __name__ == '__main__':
        unittest.main()
