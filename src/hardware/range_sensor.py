import threading
from functools import partial
import RPi.GPIO as GPIO
import time

DEBUG = False

TRIG = 23
ECHO = 24

#: cm per seconde
GELUIDSSNELHEID = 34300

global_time_start = 0
global_time_end = 0

SENSOR_FOV = 15


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
    :return: De afstand in cm
    """

    uncorrected = _get_distance_uncorrected()

    # corrigeer van onwaarschijnlijke afstand
    while uncorrected < 4 or uncorrected > 5000:
        uncorrected = _get_distance_uncorrected()

    distance = uncorrected
    return distance


def _get_distance_uncorrected() -> int:
    """
    Meet de afstand met de sensor zonder extra checks
    :return: De afstand in cm
    """
    # begin alvast te letten op de echo pin, wachten tot na de trigger kan er voor zorgen dat we de pulse missen.
    event = threading.Event()
    callback = partial(edge_callback, event)
    GPIO.add_event_detect(ECHO, GPIO.BOTH, callback=callback)

    # trigger de sensor om te meten
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    if DEBUG:
        print("Waiting for callbacks")
    completed = event.wait(timeout=0.1)  # wacht op de pulse event tot maximaal 1 seconde
    GPIO.remove_event_detect(ECHO)

    pulse_duration = global_time_end - global_time_start
    if pulse_duration < 0 or not completed:
        return -1

    distance = (pulse_duration * GELUIDSSNELHEID) / 2  # delen door twee omdat het geluid heen en terug gaat

    distance = int(distance)  # centimeter precision is realistischer

    return distance


def edge_callback(event, _):
    global global_time_start
    global global_time_end

    if GPIO.input(ECHO):
        global_time_start = time.time()
        if DEBUG:
            print("high callback")
    else:
        global_time_end = time.time()
        if DEBUG:
            print("low callback")
        # debounce door alleen te stoppen als we gestart zijn
        if global_time_start:
            event.set()


if __name__ == "__main__":
    print("measureing")
    print(get_distance())

    GPIO.cleanup()
