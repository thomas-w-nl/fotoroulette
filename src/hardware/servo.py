import configparser
import time

from src.common import log

config = configparser.ConfigParser()
config.read('fotoroulette.conf')

try:
    import RPi.GPIO as GPIO

    MAX_SERVO_POS = config['Servo'].getint('MAX_SERVO_POS')
    MIN_SERVO_POS = config['Servo'].getint('MIN_SERVO_POS')

    _position = 0

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    pwm = GPIO.PWM(18, 50)
    pwm.start(0)
except Exception:
    print("Skip loading the servo since we're in a fake environment")
    print("This is very dangerous regarding to errors. Please debug using ImportError and ModuleNotFound exeptions")


def goto_position(graden: int, sleep=0.4):
    """
    Send servo to specific position
    :param sleep:
    :param graden: de positie waar de servo heen moet draaien
    """
    global _position
    if graden > MAX_SERVO_POS or graden < MIN_SERVO_POS:
        raise IndexError("Servo: " + str(graden))
    _position = graden
    duty = _calculate_angle(graden)
    pwm.ChangeDutyCycle(duty)
    time.sleep(sleep)
    pwm.ChangeDutyCycle(0)


def get_position() -> int:
    """
    Vraag de huidige positie van de servo op
    Returns:
        De positie in graden
    """
    return _position


def _calculate_angle(angle: float) -> float:
    """
    Zet een hoek in graden om naar een duty cycle
    Args:
        angle: De hoek waar de servo heen moet draaien

    Returns:
        De duty cycle in procenten

    """
    servo_max = 10.5
    servo_min = 2.5

    servo_range = (servo_max - servo_min)
    angle_range = MAX_SERVO_POS - MIN_SERVO_POS

    servo_angle = (((angle - MIN_SERVO_POS) * servo_range) / angle_range) + servo_min

    return round(servo_angle, 1)


if __name__ == "__main__":
    while True:
        print("input:")
        x = int(input())
        goto_position(x)
        time.sleep(0.5)
