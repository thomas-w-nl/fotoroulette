# Foto Roulette Internal Communication Protocol
# FRICP
# {
#     Version:    int -         "welke versie van het FRICP is dit?";
#     Method:     str -         "get/post";
#     Request:    str -         "wat je wilt";
#     StatisCode: int -         "succes, error, not-found, etc";
#     Data:       BinaryArray - "de data die versuurd";
#     Owner:      str -         "Wie roept deze shizzel aan";
#     bufferSize: int -         "de grote van de buffer";
#     Continuous: boolean -     "of de connectie open moet worden gehouden of niet";
# }

import socket, socketserver, pickle


class Server:
    class ServerHandeler(socketserver.BaseRequestHandler):
        """
        The RequestHandler class for our server.

        It is instantiated once per connection to the server, and must
        override the handle() method to implement communication to the
        client.
        """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        # log.debug("{} wrote:".format(self.client_address[0]))
        log.debug(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

    def __init__(self):
        """
        Server class.
        Returns:
            object:
        """
        self.addr = "unixSocket"
        self.sock = socketserver.UnixStreamServer(addres, ServerHandeler)

    def createServer(self):
        self.sock.serve_forever()

    def closeServer(self):
        self.sock.server_close()

    def send(self, param):
        self.send(param)

    def __del__(self):
        pass
