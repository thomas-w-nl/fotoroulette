import RPi.GPIO as GPIO
import time

MEASUREMENTS = 3
TRIG = 23
ECHO = 24

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
    Voor naukeurigheid wordt de afstand 3x gemeten.
    :return: De afstand in cm
    """
    distance = 0
    # meet meerdere keren voor de zekerheid
    for i in range(MEASUREMENTS):
        raw = _get_distance_raw()

        while raw < 4 or raw > 5000:
            # corrigeer van onwaarschijnlijke afstand
            raw = _get_distance_raw()

        distance += raw

    distance = int(distance / MEASUREMENTS)
    return distance


def _get_distance_raw() -> int:
    """
    Meet de afstand met de sensor zonder extra checks
    :return: De afstand in cm
    """
    # begin alvast te letten op de echo pin, wachten tot na de trigger kan er voor zorgen dat we de pulse missen.
    GPIO.add_event_detect(ECHO, GPIO.BOTH, callback=edge_callback)

    # trigger de sensor om te meten
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    time.sleep(0.047)  # max 8m wachten (8m / 171,50ms^-1)

    pulse_duration = global_time_end - global_time_start
    if pulse_duration < 0:
        return -1

    GPIO.remove_event_detect(ECHO)

    distance = (pulse_duration * GELUIDSSNELHEID) / 2  # delen door twee omdat het geluid heen en terug gaat

    distance = int(distance)  # centimeter precision is realistischer

    return distance


def edge_callback(channel):
    global global_time_start
    global global_time_end

    if GPIO.input(ECHO):
        global_time_start = time.time()
    else:
        global_time_end = time.time()


if __name__ == "__main__":
    print(_get_distance_raw())

    GPIO.cleanup()
