import time
import argparse
import os
import datetime
import json
import hashlib
import os
import requests
import urllib3
from shutil import copyfile

from sensors import SensorManager

CURR_DIR = os.path.dirname(__file__)


LOG_FILE_PATH = os.path.join(CURR_DIR, "log.csv")
LOG_ENABLED = False
BOOT_CONFIG_PATH = "/boot/plant.config"
ERROR_FILE_PATH = os.path.join(CURR_DIR, "error_log.txt")
API_URL = "http://127.0.0.1:8080"
# Deployment URL:
# API_URL = "https://smart-plant-1.uc.r.appspot.com/"
CONFIG_FILE_NAME = "cloud_config.json"
CONFIG_FILE_PATH = os.path.join(CURR_DIR, CONFIG_FILE_NAME)


class SystemRunner:
    def __init__(self):
        # sensor manager used to get all sensor data
        self.SM = SensorManager()

    def menu_system(self):
        # main menu and user interaction
        while True:
            # print menu
            print()
            print("Welcome to your Smart Plant. Please select an option.")
            print("1. Begin local data collection.")
            print("2. Cloud configuration center.")
            print("3. Exit.")
            # print("2. Calibrate moisture sensor.") - would be an extra feature
            select = input("Selection: ")

            # local collection
            if select == "1":
                period = input("Please type a sample rate (in seconds): ")
                try:
                    period_t = float(period)
                    self.start_sampling(period_t)
                # notify of error
                except ValueError:
                    print("Invalid number. Try again.")
            # cloud config
            elif select == "2":
                self.configure_cloud()
            # exit
            elif select == "3":
                self.clean_exit()
            else:
                # retry
                print("Invalid selection. Try again.")

    def start_sampling(self, period_t, logging=False):
        # method to start local logging of data
        # period_t parameter defines time between data samples/logs
        # logging parameter set to True if file logging is desired
        while True:
            # get sensor data
            light = round(self.SM.get_light_pct(), 2)
            humid = round(self.SM.get_humidity_pct(), 2)
            temp = round(self.SM.get_temp_val(), 2)
            moist = round(self.SM.get_moisture_pct(), 2)
            # log to file if enabled
            if(logging):
                # log with datetime
                curr_time = datetime.datetime.now().strftime("%H:%M:%S "
                                                             "%Y-%m-%d")
                curr_log_file = open(LOG_FILE_PATH, 'a')
                # write in comma separated columns
                curr_log_file.write('{},{},{},{},{},\n'.format(
                    curr_time, light, humid, temp, moist))
                curr_log_file.close()
            else:
                # print data to console if logging disabled
                print("Light %: {}".format(light))
                print("Humidity %: {}".format(humid))
                print("Moisture %: {}".format(moist))
                print("Temperature (Celsius): {}".format(temp))
            # sleep for period
            time.sleep(period_t)

    def configure_cloud(self):
        # this method is used to connect the plant with the cloud.
        # config is based on user input.
        # configuration JSON file is created.
        # if APi check fails, log error output - actually probably not since we have interactivity here
        again = True
        while again:
            # print info
            print("Welcome to the cloud configuration center.\n")
            print("Here you can enter your plant ID and activation key to link it to "
                  "the cloud and enable data uploads.")
            print("The activation details for the plants you own are available on the web "
                  "application")
            # get plant ID from user
            entered_id = input(
                "Please enter the plant ID (enter nothing to cancel): ")
            if entered_id != "":
                # get plant key/password from user
                entered_key = input(
                    "Please enter the plant activation key (enter nothing to cancel): ")
                if entered_key != "":
                    hasher = hashlib.sha256()
                    hasher.update(bytes(entered_key, 'utf-8'))
                    # Uncomment this line and comment the one after if want hashing
                    # hashed_key = hasher.hexdigest()
                    hashed_key = entered_key
                    # verify entered details
                    verified = self.verify_plant(entered_id, hashed_key)

                    if verified:
                        # save details to file if valid, exit cloud center
                        json_info = {"plant_id": entered_id,
                                     "plant_key": hashed_key}
                        with open(CONFIG_FILE_PATH, 'w+') as config_file:
                            json.dump(json_info, config_file)
                        print("Successful cloud link! \n")
                        again = False
                    else:
                        # option to try again if verification failed (invalid details)
                        print("Error: plant ID or activation key is incorrect.")
                        user_choice = input("Try again? (y/n): ")
                        if user_choice.lower() == "y":
                            again = True
                        else:
                            again = False
                else:
                    # entering nothing exits the cloud center
                    again = False
            else:
                # entering nothing exits the cloud center
                again = False

    def verify_plant(self, plant_id, key):
        # returns true or false, calls API on plant check
        # details JSON
        details = {"plant_id": plant_id,
                   "password": key
                   }
        try:
            # post details to API, get response
            response = requests.post(
                "{}/verify_plant".format(API_URL), json=details)
        except (ConnectionRefusedError,
                urllib3.exceptions.NewConnectionError,
                urllib3.exceptions.MaxRetryError,
                requests.exceptions.ConnectionError) as e:
            # catch all connection exceptions, log an error
            self.log_error("Error accessing API: {}".format(e))
            # return False for failure
            return False

        # only return True if status is good (200)
        if response.status_code == 200:
            return True
        else:
            return False

    def upload_data(self, plant_id, plant_key, date_time, light, moisture, humidity, temperature):
        # uploads a single piece of data
        # put information into JSON
        information = {"date_time": date_time,
                       "light": light,
                       "moisture": moisture,
                       "humidity": humidity,
                       "temperature": temperature,
                       "plant_id": plant_id,
                       "password": plant_key
                       }
        # post data and get response
        response = requests.post(
            "{}/save_plant_data".format(API_URL), json=information)
        # response code 201 is "Created"
        if response.status_code != 201:
            # if bad code, log error
            self.log_error("Data upload failed. Response code {}".format(
                response.status_code))

    def start_uploading(self, period_t, max_uploads=-1):
        # similar to start_sampling but uploads to cloud instead.
        # verifies plant first, if fails then log error output and exits

        # first get details from file
        credentials = None
        try:
            with open(CONFIG_FILE_PATH, "r") as config_file:
                credentials = json.load(config_file)
        except FileNotFoundError:
            # log error if credentials not found
            error_message = "Credentials file not found."
            self.log_error(error_message)
        except json.JSONDecodeError:
            error_message = "Credentials file not valid JSON."
            # log error if credentials are found but not loadable as JSON
            self.log_error(error_message)
        if credentials is not None:
            # verify credentials
            if self.verify_plant(credentials["plant_id"], credentials["plant_key"]):
                upload_count = 0
                # by default, uploads until interrupted.
                # otherwise uploads until argument of max_uploads reached
                while upload_count < max_uploads:
                    curr_time = datetime.datetime.now().strftime("%H:%M:%S "
                                                                 "%Y-%m-%d")
                    # may surround next block in try catch, catching sensor exceptions
                    # and logging them but continuing without uploading.
                    # sensor exceptions may not be necessary
                    light = round(self.SM.get_light_pct(), 2)
                    moist = round(self.SM.get_moisture_pct(), 2)
                    humid = round(self.SM.get_humidity_pct(), 2)
                    temp = round(self.SM.get_temp_val(), 2)
                    # upload data
                    self.upload_data(
                        credentials["plant_id"], credentials["plant_key"], curr_time, light, moist, humid, temp)
                    upload_count += 1
                    # wait
                    time.sleep(period_t)
            else:
                error_message = "Invalid credentials from file."
                # log error if credentials were found but are invalid
                self.log_error(error_message)
        # exit
        self.clean_exit(False)

    def log_error(self, message):
        # log the datetime+message to error_log.txt
        curr_time = datetime.datetime.now().strftime("%H:%M:%S "
                                                     "%Y-%m-%d")
        with open(ERROR_FILE_PATH, "a+") as error_file:
            error_file.write("{} $ {}\n".format(curr_time, message))

    def clean_exit(self, notify=True):
        if notify:
            print("\nClosing.")
        # cleanup sensors via manager
        self.SM.cleanup()
        exit()


def boot_config():
    # quick check to grab a config file from /boot partition.
    # this function helps users who cannot SSH/access the Pi,
    # but can access the microSD card
    if os.path.exists("/boot/plant.config"):
        print("Configuration loaded from /boot directory.")
        new_path = os.path.join(CURR_DIR, CONFIG_FILE_NAME)
        copyfile(BOOT_CONFIG_PATH, new_path)


if __name__ == '__main__':
    # check if /boot config file exists
    boot_config()
    runner = SystemRunner()

    try:
        # argument config
        parser = argparse.ArgumentParser()

        parser.add_argument("-m", "--menu", action='store_true',
                            default=False, help="Enable menu mode.")
        parser.add_argument("-f", "--file", type=str,
                            default="NONE", help="Set file logging path and enable file logging.")
        parser.add_argument("-s", "--sample-rate", type=int,
                            default=30, help="Sample rate in seconds")

        parser.add_argument("-c", "--configure", type=bool,
                            default=False, help="Configure cloud details on startup.")
        parser.add_argument("-u", "--upload", type=bool,
                            default=False, help="Automatically start uploading to cloud.")

        args = vars(parser.parse_args())

        # extra check here just so we don't go through cloud billing
        # 1800 seconds is 30 minutes
        if args["sample_rate"] < 1800:
            args["sample_rate"] = 1800

        if args["configure"]:
            # do cloud config then continue
            runner.configure_cloud()

        if args["upload"]:
            # automatically start uploading
            runner.start_uploading(args["sample_rate"])

        else:
            if args["file"] != "NONE":
                LOG_ENABLED = True
                LOG_FILE_PATH = args["file"]
                # Create file if it does not exist
                try:
                    if not os.path.exists(LOG_FILE_PATH):
                        log_file = open(LOG_FILE_PATH, 'w+')
                        log_file.write('time,light,humidity,moisture,temp,\n')
                        log_file.close()
                except FileNotFoundError:
                    runner.clean_exit()

            if args["menu"]:
                # show the menu
                runner.menu_system()
            else:
                # regular auto local logging if menu-less mode
                runner.start_sampling(args["sample_rate"], LOG_ENABLED)

    except KeyboardInterrupt:
        runner.clean_exit()
