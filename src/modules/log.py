import logging
# import sys
# import coloredlogs

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(levelname)-8s %(asctime)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
# coloredlogs.install(logger=logger)
log = logger


def __init__():
    pass

# check if file is run as module
if __name__ != "__main__":
    __init__()
else:
    crit("script should be run as module")
