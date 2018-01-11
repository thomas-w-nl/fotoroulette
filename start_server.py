# Dit bestandje moet je runnen vanaf de command-line, start een FRICP server
# argument FRICP.Owner: (choose from 'HARDWARE', 'PROCESSING', 'GUI')

# --help output:
# usage: start_server.py [-h] FRICP.Owner
#
# Start a FRICP server
#
# positional arguments:
# FRICP.Owner  Which server needs te be started.
#
# optional arguments:
# -h, --help   show this help message and exit

# from src.thread.server import Server  # <-- #TODO: RP libary missing errors
from src.thread.fricp import FRICP
from src.common.log import *
import argparse

# TODO: 'src' not a module, import errors als je vanaf de commandline runt :(
# TODO: documentatie

choices = FRICP.Owner.list()
parser = argparse.ArgumentParser(description='Start a FRICP server')
parser.add_argument("type", metavar='FRICP.Owner', type=str, nargs=1, help="Which server needs te be started.",
                    choices=choices)

args = parser.parse_args()
type = args.type[0]
# server = Server(FRICP.Owner[type])  # TODO: niet vergeten te uncommenten
# server.open_server()
log.debug("server %s init", type)
