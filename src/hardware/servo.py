import RPi.GPIO as GPIO
import time

_position = 0
MAX_SERVO_POS = 180
MIN_SERVO_POS = 0

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
