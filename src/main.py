from src.hardware.camera import Camera
import src.common.tools as tools
from src.common.log import *
import cv2

cam = Camera()

while 1:
    tools.draw_image(cam.get_frame())
    if cv2.waitKey(27) >= 0: break

log.info("great succes!")