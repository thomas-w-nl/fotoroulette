from modules.log import *
import sys
import os

log.info("Python version: " + sys.version)
log.debug("WorkingDir: " + os.getcwd())
import modules.opencv
