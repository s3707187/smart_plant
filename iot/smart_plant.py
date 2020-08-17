
import time
import argparse
import os
import datetime

from sensors import SensorManager


SM = SensorManager()

LOG_FILE_PATH = "log.csv"
LOG_ENABLED = False


def menu_system():
    print("Welcome to your Smart Plant. Please select an option.")
    print("1. Begin local data collection.")
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


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument("-m", "--menu", action='store_true',
                            default=False, help="Enable menu mode.")
        parser.add_argument("-f", "--file", type=str,
                            default="NONE", help="Set file logging path and enable file logging.")
        parser.add_argument("-s", "--sample-rate", type=int,
                            default=30, help="Sample rate in seconds")

        args = vars(parser.parse_args())

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
                print("Invalid file name.")
                SM.cleanup()
                exit()

        if args["menu"]:
            menu_system()
        else:
            start_sampling(args["sample_rate"], LOG_ENABLED)

    except KeyboardInterrupt:
        print("\nClosing.")
        SM.cleanup()
        exit()
