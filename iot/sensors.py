import sense_hat
from gpiozero import MCP3008

LDR_CHANNEL = 0
MOISTURE_CHANNEL = 7
ADC_VALS = 1024

MOISTURE_WATER_VALUE = 700.0


class SensorManager:
    def __init__(self):
        self.ldr = MCP3008(channel=LDR_CHANNEL)
        self.moisture = MCP3008(channel=MOISTURE_CHANNEL)
        self.sense = sense_hat.SenseHat()

    def get_moisture_pct(self):
        return self.moisture.value / (MOISTURE_WATER_VALUE / 1000.0) * 100.0

    def get_light_pct(self):
        return (1 - self.ldr.value) * 100.0

    def get_temp_val(self):
        temp_h = self.sense.get_temperature_from_humidity()
        temp_p = self.sense.get_temperature_from_pressure()
        temp_avg = (temp_h + temp_p) / 2.0

        return temp_avg

    def get_humidity_pct(self):
        return self.sense.get_humidity()
    
    def cleanup(self):
        self.ldr.close()
        self.moisture.close()

