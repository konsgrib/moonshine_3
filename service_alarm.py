import RPi.GPIO as GPIO
from messenger.messenger_rabbit import QueueProcessorRabbit
from config_parser import ProgramBuilder


GPIO.setmode(GPIO.BCM)


config_yaml = "programs.yaml"
cmd = ProgramBuilder(config_yaml).get_program("alarm")

qr = QueueProcessorRabbit()
qr.run_consumer(cmd)
