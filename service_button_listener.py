import os
import RPi.GPIO as GPIO
import time
import subprocess

cycle_1_bt_pin = 9
cycle_2_bt_pin = 10
cycle_3_bt_pin = 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(cycle_1_bt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cycle_2_bt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cycle_3_bt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

jobs = {cycle_1_bt_pin: "cycle1", cycle_2_bt_pin: "cycle2", cycle_3_bt_pin: "cycle3"}

press_start_time = {9: None, 10: None, 11: None}


def start_job(pin, special=False):
    """Starts a job by running a Python script."""
    if special:
        print(f"Starting test program")
        subprocess.Popen([".venv/bin/python", "main.py"])
    else:
        print(f"Starting job: {jobs[pin]}")
        env = os.environ.copy()
        env["programm"] = jobs[pin]
        subprocess.Popen([".venv/bin/python", "main.py"], env=env)


def wait_for_it():
    last_state = {9: True, 10: True, 11: True}
    debounce_time = 0.2

    while True:
        for pin in [9, 10, 11]:
            current_state = GPIO.input(pin)
            if current_state != last_state[pin]:
                if not current_state:
                    press_start_time[pin] = time.time()
                else:
                    if pin == 9:
                        press_duration = time.time() - press_start_time[pin]
                        if press_duration > 5:
                            start_job(pin, special=True)
                        else:
                            start_job(pin)
                    elif pin in [10, 11]:
                        start_job(pin)
                    press_start_time[pin] = None
                time.sleep(debounce_time)
            last_state[pin] = current_state
        time.sleep(0.01)


if __name__ == "__main__":
    try:
        wait_for_it()
    except KeyboardInterrupt:
        print("Script terminated by user")
    finally:
        GPIO.cleanup()
