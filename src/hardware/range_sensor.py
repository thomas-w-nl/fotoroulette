import random

SENSOR_ANGLE = 15


# todo dummy data, uncomments
def get_distance() -> int:
    return random.randrange(50, 200)


# import RPi.GPIO as GPIO
# import time
#
# MEASUREMENTS = 3
# TRIG = 23
# ECHO = 24
#
#
# def _init():
#     """
#     Start de GPIO pins
#     """
#     GPIO.setwarnings(False)
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(TRIG, GPIO.OUT)
#     GPIO.setup(ECHO, GPIO.IN)
#
#     GPIO.output(TRIG, False)
#
#
# _init()
#
#
# def get_distance() -> int:
#     """
#     Meet de afstand met de sensor. Hiervoor moeten Echo op pin 24 en Trig op pin 23 aangsloten zijn
#     met weerstanden. De sensor wordt geinitaliseerd bij het inladen van dit bestand.
#     Voor naukeurigheid wordt de afstand 3x gemeten.
#     :return: De afstand in cm
#     """
#     distance = 0
#     # meet meerdere keren voor de zekerheid
#     for i in range(MEASUREMENTS):
#         raw = _get_distance_raw()
#
#         while raw < 4:
#             # corrigeer van onwaarschijnlijke afstand
#             raw = _get_distance_raw()
#
#         distance += raw
#
#     distance = int(distance / MEASUREMENTS)
#     return distance
#
#
# def _get_distance_raw() -> int:
#     """
#     Meet de afstand met de sensor zonder extra checks
#     :return: De afstand in cm
#     """
#     # trigger de sensor om te meten
#     GPIO.output(TRIG, True)
#     time.sleep(0.00001)
#     GPIO.output(TRIG, False)
#
#     pulse_start = 0
#     pulse_end = 0
#
#     # de meting loopt van high tot low, de duur van de pulse is de afstand
#     i = 0
#     while GPIO.input(ECHO) == 0:
#         pulse_start = time.time()
#         i += 1
#         # timeout
#         if i > 3000:
#             pulse_start = 0
#             break
#
#     i = 0
#     while GPIO.input(ECHO) == 1:
#         pulse_end = time.time()
#         i += 1
#         # timeout
#         if i > 3000:
#             pulse_end = -1
#             break
#
#     # helaas is GPIO.wait_for_edge niet aan de gang te krijgen
#
#     pulse_duration = pulse_end - pulse_start
#
#     distance = pulse_duration * 17150 # magic geluidssnelheid factor
#
#     distance = int(distance)  # centimeter precision is realistischer
#
#     return distance
