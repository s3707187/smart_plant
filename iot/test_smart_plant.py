import unittest
from unittest import mock
import sys
import io
import os 

import smart_plant
from smart_plant import SystemRunner

TEST_CONFIG = "test_config.json"

class MockResponse():

    def __init__(self, code):
        self.status_code = code

def mock_post(url, json=None):
    if url == "{}/verify_plant".format(smart_plant.API_URL):
        if json["plant_id"] == "01" and json["password"] == "testpassword":
            return MockResponse(200)
        else:
            return MockResponse(401)
    else:
        return MockResponse(404)

def mock_verify_plant_success(plant_id, key):
    return True

def mock_verify_plant_fail(plant_id, key):
    return False

def mock_verify_plant_check(plant_id, key):
    if plant_id == "01" and key == "testpassword":
        return True
    else:
        return False

class MainSystemTest(unittest.TestCase):
    def setUp(self):
        self.sr = SystemRunner()

    def tearDown(self):
        self.sr.SM.cleanup()
        if os.path.exists(TEST_CONFIG):
            os.remove(TEST_CONFIG)


    @mock.patch('requests.post', side_effect=mock_post)
    def test_verify_success(self, mock_requests):
        verified = self.sr.verify_plant("01", "testpassword")
        self.assertTrue(verified)

    @mock.patch('requests.post', side_effect=mock_post)
    def test_verify_bad_id(self, mock_requests):
        verified = self.sr.verify_plant("00", "testpassword")
        self.assertFalse(verified)

    @mock.patch('requests.post', side_effect=mock_post)
    def test_verify_bad_pass(self, mock_requests):
        verified = self.sr.verify_plant("01", "badpassword")
        self.assertFalse(verified)
    
    @mock.patch('requests.post', side_effect=mock_post)
    def test_verify_bad_both(self, mock_requests):
        verified = self.sr.verify_plant("00", "badpassword")
        self.assertFalse(verified)

    @mock.patch('smart_plant.CONFIG_FILE_PATH', TEST_CONFIG)
    @mock.patch('smart_plant.input', create=True)
    @mock.patch('smart_plant.SystemRunner.verify_plant', side_effect=mock_verify_plant_success)
    def test_configure_cloud_success(self, mock_verify, mock_input):
        mock_input.side_effect = ["01", "testpassword"]

        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.sr.configure_cloud()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertTrue("Welcome" in output)
        self.assertTrue("Successful cloud link!" in output)

    @mock.patch('smart_plant.CONFIG_FILE_PATH', TEST_CONFIG)
    @mock.patch('smart_plant.input', create=True)
    @mock.patch('smart_plant.SystemRunner.verify_plant', side_effect=mock_verify_plant_fail)
    def test_configure_cloud_fail(self, mock_verify, mock_input):
        mock_input.side_effect = ["01", "testpassword", "n"]

        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.sr.configure_cloud()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertTrue("Welcome" in output)
        self.assertTrue("Error: plant ID or activation key is incorrect." in output)

    @mock.patch('smart_plant.CONFIG_FILE_PATH', TEST_CONFIG)
    @mock.patch('smart_plant.input', create=True)
    @mock.patch('smart_plant.SystemRunner.verify_plant', side_effect=mock_verify_plant_check)
    def test_configure_cloud_repeat(self, mock_verify, mock_input):
        mock_input.side_effect = ["01", "badpassword", "y", "22", "badpassword2", "y", "01", "testpassword"]

        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.sr.configure_cloud()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertEqual(output.count("Welcome"), 3)
        self.assertEqual(output.count("Error: plant ID or activation key is incorrect."), 2)
        self.assertTrue("Successful cloud link!" in output)

    @mock.patch('smart_plant.CONFIG_FILE_PATH', TEST_CONFIG)
    @mock.patch('smart_plant.input', create=True)
    @mock.patch('smart_plant.SystemRunner.verify_plant', side_effect=mock_verify_plant_success)
    def test_configure_cloud_file_check(self, mock_verify, mock_input):
        mock_input.side_effect = ["01", "testpassword"]

        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.sr.configure_cloud()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertTrue(os.path.exists(TEST_CONFIG))
        file_check = False
        with open(TEST_CONFIG, "r") as test_config_file:
            file_check = '{"plant_id": "01", "plant_key": "testpassword"}' in test_config_file.read()
        self.assertTrue(file_check)
        



    

if __name__ == "__main__":
    unittest.main()
