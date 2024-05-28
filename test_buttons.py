import pytest
from unittest.mock import patch, MagicMock
import subprocess
import os
import service_button_listener  # Replace with the actual name of your script

@pytest.fixture
def setup_subprocess():
    with patch('service_button_listener.subprocess.Popen') as mock_popen:
        yield mock_popen

@pytest.fixture
def setup_os():
    with patch('service_button_listener.os.environ', new_callable=dict) as mock_environ:
        yield mock_environ

def test_start_job_normal(setup_subprocess, setup_os):
    service_button_listener.jobs = {9: "cycle1", 10: "cycle2", 11: "cycle3"}
    service_button_listener.start_job(9)
    setup_subprocess.assert_called_once_with(
        [".venv/bin/python", "main.py"], 
        env=setup_os
    )
    assert setup_os["programm"] == "cycle1"

def test_start_job_special(setup_subprocess):
    service_button_listener.start_job(9, special=True)
    setup_subprocess.assert_called_once_with(
        [".venv/bin/python", "main.py"]
    )