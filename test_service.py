import pytest
from unittest.mock import MagicMock, patch
from collections import deque
import RPi.GPIO as GPIO
from logger import logger
from exception_handler import ExceptionHandler

# Import the EventLoop class
from event_loop import EventLoop

@pytest.fixture
def event_loop():
    return EventLoop()

def test_add(event_loop):
    cmd = MagicMock()
    event_loop.add(cmd)
    assert event_loop.ready == deque([cmd])

def test_clear(event_loop):
    cmd1 = MagicMock()
    cmd2 = MagicMock()
    event_loop.add(cmd1)
    event_loop.add(cmd2)
    event_loop.clear()
    assert event_loop.ready == deque()

def test_clear_until(event_loop):
    cmd1 = MagicMock()
    cmd2 = MagicMock()
    cmd3 = MagicMock()
    event_loop.add(cmd1)
    event_loop.add(cmd2)
    event_loop.add(cmd3)
    event_loop.clear_until(cmd2)
    assert event_loop.ready == deque([cmd2, cmd3])

def test_run_executes_commands(event_loop):
    cmd1 = MagicMock()
    cmd2 = MagicMock()
    event_loop.add(cmd1)
    event_loop.add(cmd2)

    with patch.object(logger, 'warning') as mock_warning:
        event_loop.run()
        mock_warning.assert_any_call(f"Executing command: {event_loop}/{cmd1}")
        mock_warning.assert_any_call(f"Executing command: {event_loop}/{cmd2}")
        cmd1.execute.assert_called_once_with(event_loop)
        cmd2.execute.assert_called_once_with(event_loop)

def test_run_handles_stop_iteration(event_loop):
    cmd = MagicMock()
    cmd.execute.side_effect = StopIteration
    event_loop.add(cmd)

    with patch('builtins.print') as mock_print:
        event_loop.run()
        mock_print.assert_called_once_with("Exiting event loop")

def test_run_handles_exceptions(event_loop):
    cmd = MagicMock()
    exception = Exception("Test exception")
    cmd.execute.side_effect = exception
    event_loop.add(cmd)

    with patch.object(ExceptionHandler, 'handle') as mock_handle:
        event_loop.run()
        mock_handle.assert_called_once_with()

def test_run_handles_keyboard_interrupt(event_loop):
    cmd = MagicMock()
    cmd.execute.side_effect = KeyboardInterrupt
    event_loop.add(cmd)

    event_loop.run()
    cmd.execute.assert_called_once_with(event_loop)