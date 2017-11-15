import RPi.GPIO as GPIO
import time


class RangeSensor:
    def __init__(self):

        GPIO.setmode(GPIO.BCM)

        self.TRIG = 23
        self.ECHO = 24

    def __del__(self):
        GPIO.cleanup()

    def get_distance(self):

        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

        GPIO.output(self.TRIG, False)
        time.sleep(2)

        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        # todo use some clever thread interrupts or something
        while GPIO.input(self.ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(self.ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        distance = round(distance, 2)

        return distance
