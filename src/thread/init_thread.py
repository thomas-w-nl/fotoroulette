from subprocess import call
from src.common.log import *
import os

# TODO: choices moet hij eigenlijk dynamish pakken van FRICP.Owners
# TODO: deze shizzel moet eigenlijk vanaf de main worden gecalt maar die durf ik niet aan te passen
# TODO: documentatie
servers_to_start = ["HARDWARE", "PROCESSING", "GUI"]
start_server = "python3 " + os.getcwd() + "/src/thread/start_server.py"
i = 1

for owner in servers_to_start:
    command = "taskset " + str(i) + " " + str(start_server) + " " + str(owner)
    log.debug(command)
    # TODO: error: FileNotFoundError line: 16
    # log.debug(call([command]))
    i += 1
