import unittest
from unittest import mock

import smart_plant
from smart_plant import SystemRunner


class MockResponse():

    def __init__(self, code):
        self.status_code = code

def mock_get(url, json=None):
    if url == "{}/verify_plant".format(smart_plant.API_URL):
        if json["plant_id"] == "01" and json["password"] == "testpassword":
            return MockResponse(200)
        else:
            return MockResponse(401)
    else:
        return MockResponse(404)

class MainSystemTest(unittest.TestCase):
    def setUp(self):
        self.sr = SystemRunner()

    def tearDown(self):
        self.sr.SM.cleanup()

    @mock.patch('requests.get', side_effect=mock_get)
    def test_verify_success(self, mock_requests):
        verified = self.sr.verify_plant("01", "testpassword")
        self.assertTrue(verified)

    @mock.patch('requests.get', side_effect=mock_get)
    def test_verify_bad_id(self, mock_requests):
        verified = self.sr.verify_plant("00", "testpassword")
        self.assertFalse(verified)

    @mock.patch('requests.get', side_effect=mock_get)
    def test_verify_bad_pass(self, mock_requests):
        verified = self.sr.verify_plant("01", "badpassword")
        self.assertFalse(verified)
    
    @mock.patch('requests.get', side_effect=mock_get)
    def test_verify_bad_both(self, mock_requests):
        verified = self.sr.verify_plant("00", "badpassword")
        self.assertFalse(verified)

if __name__ == "__main__":
    unittest.main()
