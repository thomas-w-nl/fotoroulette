from src.thread.server import Server
from src.thread.fricp import FRICP

server = Server(FRICP.Owner.PROCESSING)
server.open_server()
