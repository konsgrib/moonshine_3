from abc import ABC, abstractmethod
from sensor.temperature import TemperatureSensor
from sensor.water import WaterLevelSensor
from sensor.humidity import HumidityLevelSensor
from sensor.button import Button
from output.two_pin.relay import Relay

from output.two_pin.relay import Relay
from output.two_pin.buzzer import Buzzer
from display.display import LcdDisplay
from messenger.messenger_file import MessengerFile


class AbstractFactory(ABC):
    @abstractmethod
    def create_device(self):
        pass


class Factory(AbstractFactory):
    device_types = {
        "TemperatureSensor": TemperatureSensor,
        "WaterLevelSensor": WaterLevelSensor,
        "HumidityLevelSensor": HumidityLevelSensor,
        "Relay": Relay,
        "Buzzer": Buzzer,
        "Button": Button,
        "LcdDisplay": LcdDisplay,
        "MessengerFile": MessengerFile,
    }

    def create_device(self, sensor_type, **kwargs):
        if sensor_type in Factory.device_types:
            try:
                return Factory.device_types[sensor_type](**kwargs)
            except Exception as e:
                print(str(e))
                raise
