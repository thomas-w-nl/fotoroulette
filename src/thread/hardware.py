from src.thread.server import Server
from src.thread.fricp import FRICP

hardware_server = Server(FRICP.Owner.HARDWARE)
hardware_server.open_server()
