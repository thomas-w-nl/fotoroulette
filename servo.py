import RPi.GPIO as GPIO
import time


class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ServoOutOfBounderyError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ServoService:
    angle = 0
    max_angle = 120
    pwm = None
    status = 'stopped'

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        self.pwm = GPIO.PWM(18, 50)
        self.pwm.start(0)

    def update(self, angle, delay = 0, step = 1):
        if angle > self.max_angle:
            raise ServoOutOfBounderyError('', 'Exceeded maximum angle of servo')

        if delay == 0:
            duty = self.calculate_angle(angle)
            self.pwm.ChangeDutyCycle(duty)
            self.angle = angle
        else:
            self.status = "started"
            for x in range(self.angle, angle, step):
                time.sleep(delay)
                duty = self.calculate_angle(x)
                self.pwm.ChangeDutyCycle(duty)
                self.angle = angle
                print(self.status)
                if self.status == "stopped":
                    break
            self.status = "stopped"




    def calculate_angle(self, angle):
        return float(angle) / 20.0 + 2.5

    def stop(self):
        self.status = "stopped"


#TODO: make the whole thing async
