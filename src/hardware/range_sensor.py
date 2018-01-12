import configparser
import threading
from functools import partial
from src.common.log import *
import time

DEBUG = False



def _init():
    """
    Start de GPIO pins
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)

    config = configparser.ConfigParser()
    config.read('fotoroulette.conf')
    TRIG = config['RangeSensor'].getint('TRIG')
    ECHO = config['RangeSensor'].getint('ECHO')
    GELUIDSSNELHEID = config['RangeSensor'].getint('GELUIDSSNELHEID')
    SENSOR_FOV = config['RangeSensor'].getint('SENSOR_FOV')

    global_time_start = 0
    global_time_end = 0


try:
    import RPi.GPIO as GPIO
    _init()
except ModuleNotFoundError:
    pass


def get_distance() -> int:
    """
    Meet de afstand met de sensor. Hiervoor moeten Echo en Trig op de geconfigureerde pins aangsloten zijn
    met weerstanden zoals in de technische tekening. De sensor wordt geinitaliseerd bij het inladen van dit bestand.

    Returns:
        De gemeten afstand in centimeters, -1 bij een error

    """
    distance = _get_distance_uncorrected()

    # corrigeer van onwaarschijnlijke afstand
    i = 0
    while distance < 4 or distance > 5000:
        distance = _get_distance_uncorrected()
        i += 1
        if i > 10:
            return -1

    return distance


def _get_distance_uncorrected() -> int:
    """
    Meet de afstand met de sensor zonder extra checks

    Returns:
        De gemeten afstand zonder checks
    """

    # begin alvast te letten op de echo pin, wachten tot na de trigger kan er voor zorgen dat we de pulse missen.
    # een event wordt aan de callback toegevoegd en geset zodra de pulse gemeten is
    event = threading.Event()
    callback = partial(_edge_callback, event)
    GPIO.add_event_detect(ECHO, GPIO.BOTH, callback=callback)

    # trigger de sensor om de afstand te meten
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    if DEBUG:
        print("Waiting for callbacks")

    # wacht op de pulse event tot maximaal 0.1 seconde (15 meter)
    completed = event.wait(timeout=0.1)
    GPIO.remove_event_detect(ECHO)

    pulse_duration = global_time_end - global_time_start
    if pulse_duration < 0 or not completed:
        return -1

    # delen door twee omdat het geluid heen en terug gaat
    distance = int((pulse_duration * GELUIDSSNELHEID) / 2)
    return distance


def _edge_callback(event, _):
    """
    Meet de falling en rising events
    Args:
        event: De event die geset wordt als de falling edge gemeten is
        _: De pin waarop de callback wordt uigevoerd
    """
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


def _destructor():
    """
    Destruct de range sensor
    """
    GPIO.remove_event_detect(ECHO)
    GPIO.cleanup()


if __name__ == "__main__":
    print("measureing")
    print(get_distance())

    GPIO.cleanup()
