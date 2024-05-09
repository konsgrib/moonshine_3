from abc import ABC, abstractmethod
import json
import operator
from typing import List
from output.two_pin.abstract_two_pin import AbstractTwoPin
from sensor.abstract_sensor import AbstractSensor
from time import sleep
from display.abstract_display import AbstractDisplay
from messenger.abstract_messenger import AbstractMessenger
from messenger.messenger_rabbit import QueueProcessorRabbit


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class RecurringCommand(Command):
    def __init__(self, commands, repeat_times=None):
        self.commands = commands
        self.repeat_times = repeat_times

    def execute(self, event_loop):
        if self.repeat_times:
            for command in self.commands:
                for _ in range(self.repeat_times):
                    event_loop.add(command)
        else:
            for command in self.commands:
                event_loop.add(self)


class ProducerCommand(Command):
    def __init__(
        self,
        termo_1: AbstractSensor,
        termo_2: AbstractSensor,
        humidity_1: AbstractSensor,
        buzzer_1: AbstractTwoPin,
        relay_pwr: AbstractTwoPin,
        relay_clr: AbstractTwoPin,
        relay_v1: AbstractTwoPin,
        relay_v2: AbstractTwoPin,
        messenger: AbstractMessenger
        ):
        self.termo_1 = termo_1
        self.termo_2 = termo_2
        self.humidity_1 = humidity_1
        self.buzzer_1 = buzzer_1
        self.relay_pwr = relay_pwr
        self.relay_clr = relay_clr
        self.relay_v1 = relay_v1
        self.relay_v2 = relay_v2
        self.messenger = messenger
        self.queue_processor = QueueProcessorRabbit()

    def execute(self, data=None):
        values = {
            "termo_1": self.termo_1.get_value().value,
            "termo_2": self.termo_2.get_value().value,
            "humidity_1": self.humidity_1.get_value().value,
            "buzzer_1" : self.buzzer_1.get_value().value,
            "relay_pwr": self.relay_pwr.get_value().value,
            "relay_clr": self.relay_clr.get_value().value,
            "relay_v1": self.relay_v1.get_value().value,
            "relay_v2": self.relay_v2.get_value().value,
            "message": self.messenger.get_message(),
        }
        message = json.dumps(values)
        sleep(1)
        self.queue_processor.produce_message(message)


class DisplayDataCommand(Command):
    def __init__(
        self,
        display: AbstractDisplay
    ):
        self.display = display

    def execute(self, data):
        message = json.loads(data)
        self.display.show_data(message)


class AlarmCommand(Command):
    rules = {
        "lt": operator.lt,
        "ge": operator.ge
    }
    def __init__(self, relay_pwr: AbstractTwoPin, buzzer: AbstractTwoPin, treshold: float, rule: str):
        self.relay_pwr = relay_pwr
        self.buzzer = buzzer
        self.treshold = treshold
        if rule in self.rules:
            self.rule = self.rules[rule]
        else:
            raise ValueError(f"Incorrect comparison rule {rule}"
                             f"must be in {list(__class__.__name__.rules.keys())}")

    def execute(self, data):
        message = json.loads(data)
        print(message)
        humidity_level = message["humidity_1"]
        if self.rule(humidity_level, self.treshold):
            if message["relay_pwr"] == 0:
                self.relay_pwr.set_state(0)
            if message["buzzer_1"] != 1:
                self.buzzer.set_state(1)
        else:
            if message["buzzer_1"] != 0:
                self.buzzer.set_state(0)


class BlockingStateUpdateCommand(Command):
    def __init__(self, sensor: AbstractSensor, treshold: float):
        self.sensor = sensor
        self.treshold = treshold

    def execute(self, event_loop):
        while self.sensor.get_value().value < self.treshold:
            print("SENSOR VALUE: ", self.sensor.get_value().value)
            sleep(1)


class PrintCommand(Command):
    def __init__(self, device: AbstractMessenger, text: str):
        self.text = text
        self.device = device

    def execute(self, event_loop):
        self.device.send_message(self.text)


class ReactCommand(Command):
    def __init__(self, sensor_name:str, relay: AbstractTwoPin,  treshold: float, rule: str, action: str):
        self.sensor_name = sensor_name
        self.relay = relay
        self.treshold = treshold
        self.queue_processor = QueueProcessorRabbit()
        self.action = action
        if rule in AlarmCommand.rules:
            self.rule = AlarmCommand.rules[rule]
        else:
            raise ValueError(f"Incorrect comparison rule {rule}"
                             f"must be in {list(__class__.__name__.rules.keys())}")
        
    def execute(self, data=None):
        data = self.queue_processor.get_message()
        message = json.loads(data)
        while not self.rule(message[self.sensor_name], self.treshold):
            data = self.queue_processor.get_message()
            message = json.loads(data)        
        if self.action == "on":
            self.relay.set_state(1)
        elif self.action == "off":
            self.relay.set_state(0)


class OutputDeviceCommand(Command):
    def __init__(self, device: AbstractTwoPin, action: str, delay: int = 0) -> None:
        self.device = device
        self.action = action
        self.delay = delay

    def execute(self, event_loop):
        if self.action == "on":
            self.device.set_state(1)
        elif self.action == "off":
            self.device.set_state(0)
        elif self.action == "onoff":
            self.device.set_state(1)
            sleep(self.delay)
            self.device.set_state(0)
        else:
            raise ValueError(f"Incorrect command: {self.action}")


class BlockingCounterAVGCommand(Command):
    def __init__(self, sensor: AbstractSensor):
        self.sensor = sensor
        self.values = []
        self.average_value = 0.0

    def execute(self, event_loop):
        for _ in range(10):
            self.values.append(self.sensor.get_value().value)
        self.average_value = sum(self.values) / len(self.values)

        while self.sensor.get_value().value < self.average_value + 0.3:
            print(
                f"SENSOR VALUE: {self.sensor.get_value().value} AVG: {self.average_value}"
            )
            self.values.append(self.sensor.get_value().value)
            self.average_value = sum(self.values) / len(self.values)



class DelayCommand(Command):
    def __init__(self, time_seconds: int) -> None:
        self.time_seconds = time_seconds

    def execute(self, event_loop):
        print("DelayCommand")
        sleep(self.time_seconds)


class ClearQueue(Command):
    def execute(self, event_loop):
        print("ClearQueue")
        event_loop.clear()  


class CommandFactory:
    def create_command(self, type, parameters):
        print(f"TYPE:{type},  PARAMS: {parameters}")
        if type == "AlarmCommand":
            return AlarmCommand(**parameters)
        elif type == "DisplayDataCommand":
            return DisplayDataCommand(**parameters)
        elif type == "ProducerCommand":
            return ProducerCommand(**parameters)
        elif type == "RecurringCommand":
            return RecurringCommand(**parameters)
        elif type == "ReactCommand":
            return ReactCommand(**parameters)
        elif type == "PrintCommand":
            return PrintCommand(**parameters)
        elif type == "OutputDeviceCommand":
            return OutputDeviceCommand(**parameters)
        elif type == "BlockingStateUpdateCommand":
            return BlockingStateUpdateCommand(**parameters)
        elif type == "BlockingCounterAVGCommand":
            return BlockingCounterAVGCommand(**parameters)
        elif type == "DelayCommand":
            return DelayCommand(**parameters)
        elif type == "ClearQueue":
            return ClearQueue(**parameters)
        else:
            raise ValueError("Unknown type", type)
