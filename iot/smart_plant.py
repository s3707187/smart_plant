import time
import argparse
import os
import datetime
import json
import hashlib
import os
import requests
import urllib3

from sensors import SensorManager

CURR_DIR = os.path.dirname(__file__)

# SM = SensorManager()

LOG_FILE_PATH = os.path.join(CURR_DIR, "log.csv")
LOG_ENABLED = False

ERROR_FILE_PATH = os.path.join(CURR_DIR, "error_log.txt")
API_URL = "http://127.0.0.1:8080"

CONFIG_FILE_PATH = os.path.join(CURR_DIR, "cloud_config.json")

class SystemRunner:
    def __init__(self):
        self.SM = SensorManager()

    def menu_system(self):
        

        while True:
            print()
            print("Welcome to your Smart Plant. Please select an option.")
            print("1. Begin local data collection.")
            print("2. Cloud configuration center.")
            print("3. Exit.")
            # print("2. Calibrate moisture sensor.") - would be an extra feature
            select = input("Selection: ")

            if select == "1":
                period = input("Please type a sample rate (in seconds): ")
                try:
                    period_t = float(period)
                    self.start_sampling(period_t)

                except ValueError:
                    print("Invalid number. Try again.")
            elif select == "2":
                self.configure_cloud()
            elif select == "3":
                self.clean_exit()
            else:
                print("Invalid selection. Try again.")


    def start_sampling(self, period_t, logging=False):
        while True:

            light = round(self.SM.get_light_pct(), 2)
            humid = round(self.SM.get_humidity_pct(), 2)
            temp = round(self.SM.get_temp_val(), 2)
            moist = round(self.SM.get_moisture_pct(), 2)

            if(logging):
                curr_time = datetime.datetime.now().strftime("%H:%M:%S "
                                                            "%Y-%m-%d")
                curr_log_file = open(LOG_FILE_PATH, 'a')
                curr_log_file.write('{},{},{},{},{},\n'.format(
                    curr_time, light, humid, temp, moist))
                curr_log_file.close()
            else:
                print("Light %: {}".format(light))
                print("Humidity %: {}".format(humid))
                print("Moisture %: {}".format(moist))
                print("Temperature (Celsius): {}".format(temp))

            time.sleep(period_t)


    def configure_cloud(self):
        # connect the plant with the cloud for the first time *
        # get user input *
        # create the config JSON file, put JSON config information *
        # if APi check fails, log error output - actually probably not since we have interactivity here
        again = True
        while again:
            print("Welcome to the cloud configuration center.\n")
            print("Here you can enter your plant ID and activation key to link it to "
                "the cloud and enable data uploads.")
            print("The activation details for the plants you own are available on the web "
                "application")

            entered_id = input(
                "Please enter the plant ID (enter nothing to cancel): ")
            if entered_id != "":
                entered_key = input(
                    "Please enter the plant activation key (enter nothing to cancel): ")
                if entered_key != "":
                    # may hash entered key here
                    hasher = hashlib.sha256()
                    hasher.update(bytes(entered_key, 'utf-8'))
                    # Uncomment this line and comment the following if want hashing
                    # hashed_key = hasher.hexdigest()
                    hashed_key = entered_key

                    verified = self.verify_plant(entered_id, hashed_key)

                    if verified:
                        json_info = {"plant_id": entered_id,
                                    "plant_key": hashed_key}
                        with open(CONFIG_FILE_PATH, 'w+') as config_file:
                            json.dump(json_info, config_file)
                        print("Successful cloud link! \n")
                        again = False
                    else:
                        print("Error: plant ID or activation key is incorrect.")
                        user_choice = input("Try again? (y/n): ")
                        if user_choice.lower() == "y":
                            again = True
                        else:
                            again = False
                else:
                    again = False
            else:
                again = False


    def verify_plant(self, plant_id, key):
        # returns true or false, calls API on plant check

        details = {"plant_id": plant_id,
                "password": key
                }
        try:
            response = requests.post("{}/verify_plant".format(API_URL), json=details)
        except (ConnectionRefusedError, 
                urllib3.exceptions.NewConnectionError, 
                urllib3.exceptions.MaxRetryError,
                requests.exceptions.ConnectionError) as e:
            self.log_error("Error accessing API: {}".format(e))
            return False

        if response.status_code == 200:
            return True
        else:
            return False

        # return True


    def upload_data(self, date_time, light, moisture, humidity, temperature):
        # uploads a single peice of data, should only be called if
        # plant configuration is verified

        information = {"date_time": date_time,
                    "light": light,
                    "moisture": moisture,
                    "humidity": humidity,
                    "temperature": temperature
                    }
        response = requests.post(
            "{}/save_plant_details".format(API_URL), json=information)

        if response.status_code != 200:
            self.log_error("Data upload failed. Response code {}".format(
                response.status_code))


    def start_uploading(self, period_t):
        # similar to start_sampling but uploads to cloud instead
        # verifies plant first, if fails then log error output and exits
        # may throw exceptions from sensors, catch here

        # first get details from file
        credentials = None
        try:
            with open(CONFIG_FILE_PATH, "r") as config_file:
                credentials = json.load(config_file)
        except FileNotFoundError:
            error_message = "Credentials file not found."
            self.log_error(error_message)
        except json.JSONDecodeError:
            error_message = "Credentials file not valid JSON."
            self.log_error(error_message)
        if credentials is not None:
            if self.verify_plant(credentials["plant_id"], credentials["plant_key"]):
                while True:
                    curr_time = datetime.datetime.now().strftime("%H:%M:%S "
                                                                "%Y-%m-%d")
                    # may surround next block in try catch, catching sensor exceptions
                    # and logging them but continuing without uploading
                    light = round(self.SM.get_light_pct(), 2)
                    moist = round(self.SM.get_moisture_pct(), 2)
                    humid = round(self.SM.get_humidity_pct(), 2)
                    temp = round(self.SM.get_temp_val(), 2)

                    self.upload_data(curr_time, light, moist, humid, temp)

                    time.sleep(period_t)
            else:
                error_message = "Invalid credentials from file."
                self.log_error(error_message)

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
        self.SM.cleanup()
        exit()


if __name__ == '__main__':
    runner = SystemRunner()

    try:
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
                runner.menu_system()
            else:
                runner.start_sampling(args["sample_rate"], LOG_ENABLED)

    except KeyboardInterrupt:
        runner.clean_exit()