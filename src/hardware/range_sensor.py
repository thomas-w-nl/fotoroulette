def get_distance() -> int:
    return 10


# todo dummy data, remove 2 triple quotes and 2 backslashes
"""
import RPi.GPIO as GPIO
import time

MEASUREMENTS = 3
TRIG = 23
ECHO = 24

# init
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)


def get_distance() -> int:

    \"""
    Meet de afstand met de sensor. Hiervoor moeten Echo op pin 24 en Trig op pin 23 aangsloten zijn
    met weerstanden. De sensor wordt geinitaliseerd bij het inladen van dit bestand.
    Voor naukeurigheid wordt de afstand 3x gemeten.
    :return: int: de afstand in cm
    \"""
    distance = 0

    for i in range(MEASUREMENTS):
        raw = _get_distance_raw()

        while raw < 2:
            # recover from improbable distance
            raw = _get_distance_raw()

        distance += raw

    distance = int(distance / MEASUREMENTS)
    # todo dummy data
    return 10


def _get_distance_raw() -> int:
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = 0
    pulse_end = 0

    i = 0
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        i += 1
        if i > 3000:
            pulse_start = 0
            break

    i = 0
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        i += 1
        if i > 3000:
            pulse_end = -1
            break


    # helaas is GPIO.wait_for_edge niet aan de gang te krijgen

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = int(distance)  # centimeter precision is good enough

    return distance
"""
