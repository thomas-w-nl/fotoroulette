import subprocess
from src.common.log import *
import os
from src.thread.fricp import FRICP
import datetime


def start(servers_to_start: list() = FRICP.Owner.list(), start_from_core: int = 1) -> list():
    """
    Start servers op verschillende cores (optellent vanaf `start_from_core`), geef een Array mee met welke servers er moeten worden gestart.
    Bij geen argumenten start hij alle servers.

    Args:
        servers_to_start(list): HARDWARE, PROCESSING of GUI, default is alles
        start_from_core(int): vanaf welke core moeten de servers worden gestart, default is 0

    Returns:
        list(int): array(1,0) succes codes, of de command om de servers te starten succesvol is uitgevoerd. (0 is succes)
    """
    script_location = os.getcwd() + "/start_server.py"
    succes = []
    i = start_from_core
    for owner in servers_to_start:
        file = str(datetime.datetime.now()) + "." + str(owner) + ".server.log"
        log_file = open(os.getcwd() + "/logs/" + file, "w")
        command = ["taskset", str(i), "python3", script_location, owner]
        log.debug(command)
        succes.append(subprocess.call(command, stdout=log_file))
        i += 1
    return succes
