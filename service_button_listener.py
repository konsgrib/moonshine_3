#!/usr/bin/env python3

import os
import RPi.GPIO as GPIO
import time
from datetime import datetime
from logger import logger

import subprocess


cycle_1_bt_pin = 9
cycle_2_bt_pin = 10
# cycle_3_bt_pin = 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(cycle_1_bt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cycle_2_bt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(cycle_3_bt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)





jobs = {
    cycle_1_bt_pin: "cycle1",
    cycle_2_bt_pin: "cycle1",
    cycle_3_bt_pin: "cycle3"
}

last_pressed = time.time()

def callback(channel):
    global last_pressed
    button_state = GPIO.input(channel)
    if button_state == False and time.time() - last_pressed > 1.0:  # 1.0 second debounce period
        last_pressed = time.time()
        logger.warning(f"{jobs[channel]} will be executed")
        env = os.environ.copy()
        env["programm"] = jobs[channel]
        try:
            s = subprocess.Popen(["/home/pi/Projects/moonshine_3/.venv/bin/python",
                            "/home/pi/Projects/moonshine_3/main.py",
                            ],
                           env=env
                            )
            s.wait()
            logger.warning(f"{{jobs[channel]}} finished with code {s.returncode}")
        except Exception as e:
            logger.error(f"ERROR CALLING PRGRAM: {str(e)}")



GPIO.add_event_detect(cycle_1_bt_pin, GPIO.BOTH, callback=callback)
GPIO.add_event_detect(cycle_2_bt_pin, GPIO.BOTH, callback=callback)
# GPIO.add_event_detect(cycle_3_bt_pin, GPIO.BOTH, callback=callback)

while True:
    time.sleep(1)