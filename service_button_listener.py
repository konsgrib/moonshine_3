#!/usr/bin/env python3

import os
import RPi.GPIO as GPIO
import time
from datetime import datetime

import subprocess


cycle_1_bt_pin = 9
cycle_2_bt_pin = 10
cycle_3_bt_pin = 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(cycle_1_bt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cycle_2_bt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cycle_3_bt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)





jobs = {
    cycle_1_bt_pin: "/home/pi/Projects/moonshine/cycle_1.py",
    cycle_2_bt_pin: "/home/pi/Projects/moonshine/cycle_2.py",
    cycle_3_bt_pin: "/home/pi/Projects/moonshine/cycle_3.py"
}

last_pressed = time.time()

def callback(channel):
    global last_pressed
    button_state = GPIO.input(channel)
    if button_state == False and time.time() - last_pressed > 1.0:  # 1.0 second debounce period
        last_pressed = time.time()
        print(f"{jobs[channel]} will be executed")
        # subprocess.Popen(["/home/pi/Projects/moonshine/.venv/bin/python",
        #                 jobs[channel],
        #             ]
        #         )              




GPIO.add_event_detect(cycle_1_bt_pin, GPIO.BOTH, callback=callback)
GPIO.add_event_detect(cycle_2_bt_pin, GPIO.BOTH, callback=callback)
GPIO.add_event_detect(cycle_3_bt_pin, GPIO.BOTH, callback=callback)

while True:
    time.sleep(1)
    now = datetime.now()