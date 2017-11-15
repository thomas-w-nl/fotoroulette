import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, max_angle=120, step=5, delay=0):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        self.pwm = GPIO.PWM(18, 50)
        self.pwm.start(0)

        self.max_angle = 120
        self.angle = 0
        self.step = step
        self.delay = delay

    def __next__(self):
        if self.angle > self.max_angle:
            raise StopIteration

        self.angle += self.step

        time.sleep(self.delay)
        duty = self.angle / 20.0 + 2.5
        self.ChangeDutyCycle(duty)

        return self.angle

    def __iter__(self):
        return self


if __name__ == "__main__":
    servo = Servo()

    for angle in servo:
        print(angle)

#TODO: make the whole thing async
