import sense_hat
from gpiozero import MCP3008

# MCP3008 channel for light sensor
LDR_CHANNEL = 0
# MCP3008 channel for moisture sensor
MOISTURE_CHANNEL = 7

MOISTURE_WATER_VALUE = 700.0


class SensorManager:
    # this class managers all sensors, serves as an interface to them.

    def __init__(self):
        self.ldr = MCP3008(channel=LDR_CHANNEL)
        self.moisture = MCP3008(channel=MOISTURE_CHANNEL)
        self.sense = sense_hat.SenseHat()

    def get_moisture_pct(self):
        # convert moisture value to a %.
        # MOISTURE_WATER_VALUE is where the medium is pure water (max value)
        # this value is 700 based on moisture sensor specification
        return self.moisture.value / (MOISTURE_WATER_VALUE / 1000.0) * 100.0

    def get_light_pct(self):
        # light sensor gives 'amount of darkness', conver here to '% of light'
        return (1 - self.ldr.value) * 100.0

    def get_temp_val(self):
        # get the average of the two temperature sources on Sense HAT
        temp_h = self.sense.get_temperature_from_humidity()
        temp_p = self.sense.get_temperature_from_pressure()
        temp_avg = (temp_h + temp_p) / 2.0

        return temp_avg

    def get_humidity_pct(self):
        return self.sense.get_humidity()

    def cleanup(self):
        self.ldr.close()
        self.moisture.close()
