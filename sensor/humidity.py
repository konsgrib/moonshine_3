import adafruit_dht
import board
from .abstract_sensor import AbstractSensor, SensorValue
from time import sleep


class HumidityLevelSensor(AbstractSensor):
    def __init__(self, pin):
        self.pin = pin
        self.sensor = adafruit_dht.DHT22(
            getattr(board, f"D{self.pin}"), use_pulseio=False
        )

    def get_value(self) -> SensorValue:

        try:
            humidity = self.sensor.humidity
            return SensorValue(200, round(humidity, 1), "OK")
        except RuntimeError:
            return SensorValue(500, -1, "NOK")
        finally:
            sleep(1)
