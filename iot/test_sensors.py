import unittest
from sensors import SensorManager



class SensorManagerTest(unittest.TestCase):
    def setUp(self):
        self.sm = SensorManager()

    def tearDown(self):
        self.sm = None

    def test_get_moisture_pct(self):
        moisture = self.sm.get_moisture_pct()
        valid_result = moisture >= 0 and moisture <= 100
        self.assertTrue(valid_result)

    def test_get_light_pct(self):
        light = self.sm.get_light_pct()
        valid_result = light >= 0 and light <= 100
        self.assertTrue(valid_result)

    def test_get_temp_val(self):
        temp = self.sm.get_temp_val()
        # 0 Kelvin and melting temperature of copper
        valid_result = temp >= -273.16 and temp <= 1086
        self.assertTrue(valid_result)

    def test_get_humidity_pct(self):
        humidity = self.sm.get_humidity_pct()
        valid_result = humidity >= 0 and humidity <= 100
        self.assertTrue(valid_result)

if __name__ == "__main__":
    unittest.main()
