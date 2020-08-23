
import time
import argparse
import os
import datetime
import json
import hashlib
import requests

from sensors import SensorManager


SM = SensorManager()

LOG_FILE_PATH = "log.csv"
LOG_ENABLED = False

ERROR_FILE_PATH = "error_log.csv"
API_URL = "http://url.com"

CONFIG_FILE_PATH = "cloud_config.json"


def menu_system():
    print("Welcome to your Smart Plant. Please select an option.")
    print("1. Begin local data collection.")
    print("2. Cloud configuration center.")
    print("3. Exit.")
    # print("2. Calibrate moisture sensor.") - would be an extra feature

    while True:
        select = input("Selection: ")

        if select == "1":
            period = input("Please type a sample rate (in seconds): ")
            try:
                period_t = float(period)
                start_sampling(period_t)

            except ValueError:
                print("Invalid number. Try again.")
        elif select == "2":
            configure_cloud()
        elif select == "3":
            clean_exit()
        else:   
            print("Invalid selection. Try again.")


def start_sampling(period_t, logging=False):
    while True:

        light = round(SM.get_light_pct(), 2)
        humid = round(SM.get_humidity_pct(), 2)
        temp = round(SM.get_temp_val(), 2)
        moist = round(SM.get_moisture_pct(), 2)

        if(LOG_ENABLED):
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


def configure_cloud():
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

        entered_id = input("Please enter the plant ID (enter nothing to cancel): ")
        if entered_id != "":
            entered_key = input("Please enter the plant activation key (enter nothing to cancel): ")
            if entered_key != "":
                # may hash entered key here
                hasher = hashlib.sha256()
                hasher.update(bytes(entered_key, 'utf-8'))
                hashed_key = hasher.hexdigest()

                verified = verify_plant(entered_id, hashed_key)

                if verified:
                    json_info = {"plant_id": entered_id,
                                 "plant_key": hashed_key}
                    with open(CONFIG_FILE_PATH, 'w+') as config_file:
                        json.dump(json_info, config_file)
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

def verify_plant(plant_id, hashed_key):
    # returns true or false, calls API on plant check

    # response = requests.get("{}/verify_plant".format(API_URL), auth=(plant_id, hashed_key))
    # if response.status_code == 200:
    #     return True
    # else:
    #     return False

    return True


def upload_data():
    # uploads a single peice of data, should only be called if
    # plant configuration is verified
    pass


def start_uploading():
    # similar to start_sampling but uploads to cloud instead
    # verifies plant first, if fails then log error output and exits
    # may throw exceptions from sensors, catch here
    pass


def log_error(message):
    # log the datetime+message to error_log.txt?
    curr_time = datetime.datetime.now().strftime("%H:%M:%S "
                                                 "%Y-%m-%d")
    with open(ERROR_FILE_PATH, "a+") as error_file:
        error_file.write("{} $ {}".format(curr_time, message))
    

def clean_exit():
    print("\nClosing.")
    SM.cleanup()
    exit()

if __name__ == '__main__':
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
        if args["configure"]:
            # do cloud config then continue
            configure_cloud()

        if args["upload"]:
            # automatically start uploading
            start_uploading()

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
                    clean_exit()

            if args["menu"]:
                menu_system()
            else:
                start_sampling(args["sample_rate"], LOG_ENABLED)

    except KeyboardInterrupt:
        clean_exit()
