import pytest
from unittest.mock import MagicMock, patch
from command_factory import CommandFactory, AlarmCommand, DisplayDataCommand, ProducerCommand, RecurringCommand, ReactCommand, PrintCommand, OutputDeviceCommand, BlockingStateUpdateCommand, BlockingCounterAVGCommand, DelayCommand, ClearQueue

@pytest.fixture
def command_factory():
    return CommandFactory()

def test_create_alarm_command(command_factory):
    parameters = {
        "relay_pwr": MagicMock(),
        "buzzer": MagicMock(),
        "treshold": 50.0,
        "rule": "lt"
    }
    command = command_factory.create_command("AlarmCommand", parameters)
    assert isinstance(command, AlarmCommand)
    assert command.treshold == 50.0
    assert command.rule == AlarmCommand.rules["lt"]

def test_create_display_data_command(command_factory):
    parameters = {
        "display": MagicMock()
    }
    command = command_factory.create_command("DisplayDataCommand", parameters)
    assert isinstance(command, DisplayDataCommand)
    assert command.display == parameters["display"]

def test_create_producer_command(command_factory):
    parameters = {
        "termo_1": MagicMock(),
        "termo_2": MagicMock(),
        "humidity_1": MagicMock(),
        "buzzer_1": MagicMock(),
        "relay_pwr": MagicMock(),
        "relay_clr": MagicMock(),
        "relay_v1": MagicMock(),
        "relay_v2": MagicMock(),
        "messenger": MagicMock()
    }
    command = command_factory.create_command("ProducerCommand", parameters)
    assert isinstance(command, ProducerCommand)
    assert command.termo_1 == parameters["termo_1"]

def test_create_recurring_command(command_factory):
    parameters = {
        "commands": [MagicMock()],
        "repeat_times": 5
    }
    command = command_factory.create_command("RecurringCommand", parameters)
    assert isinstance(command, RecurringCommand)
    assert command.repeat_times == 5

def test_create_react_command(command_factory):
    parameters = {
        "sensor_name": "sensor_1",
        "relay": MagicMock(),
        "treshold": 30.0,
        "rule": "ge",
        "action": "on"
    }
    command = command_factory.create_command("ReactCommand", parameters)
    assert isinstance(command, ReactCommand)
    assert command.sensor_name == "sensor_1"

def test_create_print_command(command_factory):
    parameters = {
        "device": MagicMock(),
        "text": "2,1"
    }
    command = command_factory.create_command("PrintCommand", parameters)
    assert isinstance(command, PrintCommand)
    assert command.text == "2,1"

def test_create_output_device_command(command_factory):
    parameters = {
        "device": MagicMock(),
        "action": "on",
        "delay": 10
    }
    command = command_factory.create_command("OutputDeviceCommand", parameters)
    assert isinstance(command, OutputDeviceCommand)
    assert command.action == "on"
    assert command.delay == 10

def test_create_blocking_state_update_command(command_factory):
    parameters = {
        "sensor": MagicMock(),
        "treshold": 25.0
    }
    command = command_factory.create_command("BlockingStateUpdateCommand", parameters)
    assert isinstance(command, BlockingStateUpdateCommand)
    assert command.treshold == 25.0

def test_create_blocking_counter_avg_command(command_factory):
    parameters = {
        "sensor": MagicMock()
    }
    command = command_factory.create_command("BlockingCounterAVGCommand", parameters)
    assert isinstance(command, BlockingCounterAVGCommand)
    assert command.sensor == parameters["sensor"]

def test_create_delay_command(command_factory):
    parameters = {
        "time_seconds": 5
    }
    command = command_factory.create_command("DelayCommand", parameters)
    assert isinstance(command, DelayCommand)
    assert command.time_seconds == 5

def test_create_clear_queue_command(command_factory):
    parameters = {}
    command = command_factory.create_command("ClearQueue", parameters)
    assert isinstance(command, ClearQueue)