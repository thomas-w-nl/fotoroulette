import RPi.GPIO as GPIO
import time

_position = 0
_max_position = 175
_min_position = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 50)
pwm.start(0)


def goto_position(graden: int):
    """
    Send servo to specific position
    :param graden: de positie waar de servo heen moet draaien
    """
    if (graden > _max_position or graden < _min_position):
        raise IndexError("Servo: " + str(graden))
    _position = graden
    duty = calculate_angle(graden)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.4)


def get_position() -> int:
    """
    Get current servo position
    :return de positie van de servo
    """
    return _position


def increase_position(graden: int) -> int:
    """
    Increase position of servo by amount of degrees
    :param graden: aantal graden waarbij de servo moet gaan draaien
    :return de nieuwe positie in graden
    """
    goto_position(get_position() + graden)
    return get_position()


def calculate_angle(angle):
    """
    Calculation of degrees
    :param angle: De hoek die omgezet moet worden
    :return de waarde die de servo verwacht
    """
    return float(angle) / 20.0 + 2.5


if __name__ == "__main__":
    while True:
        print("input:")
        x = int(input())
        goto_position(x)
        time.sleep(0.5)
