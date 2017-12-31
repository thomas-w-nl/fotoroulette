import configparser

import RPi.GPIO as GPIO
import time

servo_config = configparser.ConfigParser().read('fotoroulette.conf')['Servo']
MAX_SERVO_POS = servo_config['MAX_SERVO_POS']
MIN_SERVO_POS = servo_config['MIN_SERVO_POS']

_position = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 50)
pwm.start(0)


def goto_position(graden: int, sleep=0.4):
    """
    Send servo to specific position
    :param sleep:
    :param graden: de positie waar de servo heen moet draaien
    """
    global _position
    if (graden > MAX_SERVO_POS or graden < MIN_SERVO_POS):
        raise IndexError("Servo: " + str(graden))
    _position = graden
    duty = calculate_angle(graden)
    pwm.ChangeDutyCycle(duty)
    time.sleep(sleep)
    pwm.ChangeDutyCycle(0)


def get_position() -> int:
    return _position


def calculate_angle(angle: float) -> float:
    """
    Zet een hoek in graden om naar een duty cycle
    Args:
        angle: De hoek waar de servo heen moet draaien

    Returns:
        De duty cycle in procenten

    """
    servo_max = 10.5
    servo_min = 2.5
    angle_max = MAX_SERVO_POS
    angle_min = MIN_SERVO_POS

    servo_range = (servo_max - servo_min)
    angle_range = angle_max - angle_min

    servo_angle = (((angle - angle_min) * servo_range) / angle_range) + servo_min

    return round(servo_angle, 1)


if __name__ == "__main__":
    while True:
        print("input:")
        x = int(input())
        goto_position(x)
        time.sleep(0.5)
