import sys
from src.thread.server import *
from src.thread.fricp import *

server = Server(FRICP.Owner.PROCESSING)
server.open_server()