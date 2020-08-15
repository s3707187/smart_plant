import time
import argparse

from sensors import SensorManager


SM = SensorManager()


def menu_system():
    print("Welcome to your Smart Plant. Please select an option.")
    print("1. Begin local data collection.")
    # print("2. Calibrate moisture sensor.") - would be an extra feature

    while(True):
        select = input("Selection: ")

        if select == "1":
            period = input("Please type a sample rate (in seconds): ")
            try:
                period_t = float(period)
                while(True):
                    light = round(SM.get_light_pct(), 2)
                    humid = round(SM.get_humidity_pct(), 2)
                    temp = round(SM.get_temp_val(), 2)
                    moist = round(SM.get_moisture_pct(), 2)

                    print("Light %: {}".format(light))
                    print("Humidity %: {}".format(humid))
                    print("Moisture %: {}".format(moist))
                    print("Temperature (Celsius): {}".format(temp))
                    time.sleep(period_t)

            except ValueError:
                print("Invalid number. Try again.")

        else:
            print("Invalid selection. Try again.")

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("-m", "--menu", action='store_true',
                            help="Enable menu mode.")
    PARSER.add_argument("-f", "--file", action='store_true',
                            help="Enable saving to file.")
    ARGS = vars(PARSER.parse_args())


    try:
        menu_system()
    except KeyboardInterrupt:
        print("Closing.")
        exit()