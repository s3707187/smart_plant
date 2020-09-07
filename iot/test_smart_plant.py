import unittest
from unittest import mock
import sys
import io
import os 

import smart_plant
from smart_plant import SystemRunner

TEST_CONFIG = "test_config.json"
TEST_CONFIG_PERMANENT = os.path.join("test_files", "test_config_perm.json")
TEST_CONFIG_PERMANENT_BAD = os.path.join("test_files", "test_config_perm_bad.json")

class MockResponse():

    def __init__(self, code):
        self.status_code = code

def mock_post(url, json=None):
    if url == "{}/verify_plant".format(smart_plant.API_URL):
        if json["plant_id"] == "01" and json["password"] == "testpassword":
            return MockResponse(200)
        else:
            return MockResponse(401)

    elif url == "{}/save_plant_data".format(smart_plant.API_URL):
        if json["plant_id"] == "01" and json["password"] == "testpassword":
            return MockResponse(201)
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

class ErrorMock:
    previous_error = None
    @staticmethod
    def mock_error(message):
        ErrorMock.previous_error = message

class DataUploadMock:
    previous_upload = None
    @staticmethod
    def mock_upload(plant_id, plant_key, date_time, light, moisture, humidity, temperature):
        DataUploadMock.previous_upload = (plant_id, plant_key, date_time, light, moisture, humidity, temperature)

class MainSystemTest(unittest.TestCase):
    def setUp(self):
        self.sr = SystemRunner()

    def tearDown(self):
        self.sr.SM.cleanup()
        if os.path.exists(TEST_CONFIG):
            os.remove(TEST_CONFIG)
        ErrorMock.previous_error = None
        DataUploadMock.previous_upload = None


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
        
    ####################
    # Story 19 Tests Ahead

    @mock.patch('requests.post', side_effect=mock_post)
    @mock.patch('smart_plant.SystemRunner.log_error', side_effect=ErrorMock.mock_error)
    def test_upload_data(self, mock_error_log, mock_requests):
        self.sr.upload_data("01", "testpassword", "01:49:12 2020-08-24", 35, 50, 35, 21)
        self.assertIsNone(ErrorMock.previous_error)

    @mock.patch('requests.post', side_effect=mock_post)
    @mock.patch('smart_plant.SystemRunner.log_error', side_effect=ErrorMock.mock_error)
    def test_upload_data_invalid(self, mock_error_log, mock_requests):
        self.sr.upload_data("02", "testpassword", "01:49:12 2020-08-24", 35, 50, 35, 21)
        self.assertTrue("Data upload failed. Response code" in ErrorMock.previous_error)

    @mock.patch('smart_plant.SystemRunner.verify_plant', side_effect=mock_verify_plant_success)
    @mock.patch('smart_plant.CONFIG_FILE_PATH', TEST_CONFIG_PERMANENT)
    @mock.patch('smart_plant.SystemRunner.upload_data', side_effect=DataUploadMock.mock_upload)
    @mock.patch('smart_plant.SystemRunner.clean_exit', side_effect=None)
    @mock.patch('smart_plant.SystemRunner.log_error', side_effect=ErrorMock.mock_error)
    def test_start_uploading(self, mock_error_log, mock_exit_clean, mock_data_up, mock_verification):
        self.sr.start_uploading(1, 1)
        self.assertTrue(ErrorMock.previous_error is None)
        for i in range(0,7):
            self.assertTrue(DataUploadMock.previous_upload[i] is not None)

    @mock.patch('smart_plant.SystemRunner.verify_plant', side_effect=mock_verify_plant_success)
    @mock.patch('smart_plant.CONFIG_FILE_PATH', "none file")
    @mock.patch('smart_plant.SystemRunner.upload_data', side_effect=DataUploadMock.mock_upload)
    @mock.patch('smart_plant.SystemRunner.clean_exit', side_effect=None)
    @mock.patch('smart_plant.SystemRunner.log_error', side_effect=ErrorMock.mock_error)
    def test_start_uploading_no_creds(self, mock_error_log, mock_exit_clean, mock_data_up, mock_verification):
        self.sr.start_uploading(1, 1)
        self.assertTrue("Credentials file not found." in ErrorMock.previous_error)
        self.assertTrue(DataUploadMock.previous_upload is None)

    @mock.patch('smart_plant.SystemRunner.verify_plant', side_effect=mock_verify_plant_success)
    @mock.patch('smart_plant.CONFIG_FILE_PATH', TEST_CONFIG_PERMANENT_BAD)
    @mock.patch('smart_plant.SystemRunner.upload_data', side_effect=DataUploadMock.mock_upload)
    @mock.patch('smart_plant.SystemRunner.clean_exit', side_effect=None)
    @mock.patch('smart_plant.SystemRunner.log_error', side_effect=ErrorMock.mock_error)
    def test_start_uploading_bad_creds(self, mock_error_log, mock_exit_clean, mock_data_up, mock_verification):
        self.sr.start_uploading(1, 1)
        self.assertTrue("Credentials file not valid JSON." in ErrorMock.previous_error)
        self.assertTrue(DataUploadMock.previous_upload is None)

    
if __name__ == "__main__":
    unittest.main()
