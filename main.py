import os
import sys
import RPi.GPIO as GPIO

from config_parser import ProgramBuilder
from event_loop import EventLoop
from logger import logger


programm = os.environ.get("programm", "test")
logger.warning(f"STARTING PROGRAM: {programm}")

GPIO.setmode(GPIO.BCM)

config_yaml = "programs.yaml"
try:
    exec_program = ProgramBuilder(config_yaml).get_program(programm)
except Exception as e:
    logger.error(f"Failed to read the program: {programm} Error: {str(e)}")

el = EventLoop()
for cmd in exec_program:
    el.add(cmd)
el.run()
logger.warning(f"PROGRAM FINISHED: {programm}")
sys.exit(0)
