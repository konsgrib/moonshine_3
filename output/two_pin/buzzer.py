import RPi.GPIO as GPIO
from .abstract_two_pin import AbstractTwoPin, TwoPinValue


class Buzzer(AbstractTwoPin):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.frequency = 50
        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.stop()

    def set_state(self, new_state):
        if new_state == 1:
            self.pwm.start(50)
            self.pwm.ChangeFrequency(2800)
        else:
            self.pwm.stop()
            GPIO.output(self.pin, GPIO.LOW)

    def get_value(self) -> TwoPinValue:
        try:
            state_pin = GPIO.input(self.pin)
            return TwoPinValue(200, state_pin, "OK")
        except Exception as e:
            return TwoPinValue(500, str(e), "NOK")
