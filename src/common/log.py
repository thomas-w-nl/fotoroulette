# gebruik log om je *al* je dingen te loggen. (debug, info, warning, error en critical)
import logging
from configparser import ConfigParser

# Setting up config file

config = ConfigParser()
config.read("settings.conf")
config = config["General"]


def __init__():
    pass


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(levelname)-8s %(asctime)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=int(config['LOG_LEVEL']))
log = logger
# check if file is run as module
if __name__ != "__main__":
    __init__()
else:
    crit("script should be run as module")
