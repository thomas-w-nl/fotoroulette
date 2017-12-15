import RPi.GPIO as GPIO
import time

SENSOR_ANGLE = 15
MEASUREMENTS = 3
TRIG = 23
ECHO = 24


def _init():
    """
    Start de GPIO pins
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)


_init()


def get_distance() -> int:
    """
    Meet de afstand met de sensor. Hiervoor moeten Echo op pin 24 en Trig op pin 23 aangsloten zijn
    met weerstanden. De sensor wordt geinitaliseerd bij het inladen van dit bestand.
    Voor naukeurigheid wordt de afstand 3x gemeten.
    :return: De afstand in cm, -1 bij error
    """
    distance = 0
    # meet meerdere keren voor de zekerheid
    for i in range(MEASUREMENTS):
        raw = _get_distance_raw()

        retry_counter = 0
        while raw < 4:
            # corrigeer van onwaarschijnlijke afstand en errors
            raw = _get_distance_raw()
            if retry_counter > 5:
                return -1

        distance += raw

    distance = int(distance / MEASUREMENTS)
    return distance


def _get_distance_raw() -> int:
    """
    Meet de afstand met de sensor zonder extra checks, returned -1 bij een error
    :return: De afstand in cm
    """
    # trigger de sensor om te meten
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # de meting loopt van high tot low, de duur van de pulse is de afstand

    channel = GPIO.wait_for_edge(ECHO, GPIO.RISING, timeout=50000)
    if channel is None:
        return -1
    else:
        pulse_start = time.time()

    channel = GPIO.wait_for_edge(ECHO, GPIO.FALLING, timeout=50000)
    if channel is None:
        return -1
    else:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    print("Duration: " + str(pulse_duration))

    distance = pulse_duration * 17150  # magic geluidssnelheid factor

    distance = int(distance)  # centimeter precision is realistischer

    return distance


if __name__ == "__main__":
    print(_get_distance_raw())
