import socket, socketserver, pickle, os
from src.common.log import *
from enum import Enum


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

    class ServerStatus(Enum):
        ERROR = -2
        OFF = -1
        UNSET = 0
        ON = 1

    class FRICP():
        # Foto Roulette Internal Communication Protocol
        class Method(Enum):
            GET = 0
            POST = 1

        class StatusCode(Enum):
            UNDEFINED = 0
            SUCCES = 100

            UNKNOWN_ERROR = 200
            UNKNOWN_REQUEST = 201
            REJECTED = 202
            CONNECTION_LOST = 203
            CONNECTION_TIMEOUT = 204
            VERSION_MISMATCH = 205

            CLOSE_CONNECTION = 301

        class Request(Enum):
            HARDWARE_GET_CAMERA = auto()
            HARDWARE_GET_SERVO_POSITION = auto()
            HARDWARE_POST_CAMERA = auto()
            HARDWARE_POST_SERVO_POSITION = auto()

        class Owner(Enum):
            HARDWARE = auto()
            GUI = auto()
            PROCESSING = auto()

        def __init__(self, request, method, data, owner, statis_code=StatusCode.UNDEFINED, open=false, buffer_size=1024,
                     version=1):
            """
            Foto Roulette Internal Communication Protocol
            Protocol voor de communicatie tussen de processing; hardware en gui
            Args:
                request (Request/Enum): De request of response die je doet.
                method (Method/Enum): "GET" als je opvraagt, "POST" Als je wat vraagt
                data (Any): De data die je verstuurd.
                owner (Owner/Enum): "HARDWARE/GUI/PROCESSING" Wie het bericht verstuurd
                statis_code (:obj: `StatusCode/Enum`, optional): "UNDEFINED" Voor een request.
                    Bij een response staat de status van het bericht. Default is "UNDEFINED"
                open (:obj: `bool`, optional): true voor een continuous verbinding. Default is false
                buffer_size (:obj: `int`, optional): Hoegroot de buffer moet zijn. Default is 1024
                version (:obj: `int`, optional): De FRICP versie nummer. Default is 1
            """
            self.request = request
            self.method = method
            self.data = data
            self.owner = owner
            self.statisCode = statis_code
            self.open = open
            self.bufferSize = buffer_size
            self.version = version

            # self.binaryData =

        def __del__(self):
            pass

        def get_dictionary(self):
            """
            Krijg de directionary zodat je er wat nuttige dingen mee kan doen.
            Returns:
                dictionary: Dirtionary van het FRICP

            """
            return {'request': self.request, 'method': self.method, 'data': self.data, 'owner': self.owner,
                    'statisCode': self.statisCode, 'open': self.open, 'bufferSize': self.bufferSize,
                    'version': self.version}

        def get_binary(self):
            """
            Returns:
                binary: Krijg de dirtionary in een pickle pakketje zodat je het kan versturen
            """
            return pickle.dump(self.get_dictionary())

    def __init__(self):
        """
        Server class (zit ook de client in). Gebruikt door de hardware; gui en processing om met elkaar te praten door middel van PRICPv1
        Returns:
            Helemaal niks, jonguh BAM!
        """

        # Deze moet je overwriten als je deze class extend
        self.addr = "unixSocket"
        self.owner = "Unset"

        self._serverStatus = self._set_server_status(OFF)
        self.sock = socketserver.UnixStreamServer(self.addr, self.ServerHandeler)

    def __del__(self):
        """
        Destructor, closed alle verbinden en sluit de server af.
        """
        self.close_server()

    def open_server(self):
        """
        Open de server zodat je verbindingen kan ontvangen.
        Returns:
            ServerStatus/Enum: Zodat je kan zien of hij goed is gestart!
        """
        if self.get_server_status() > self.ServerStatus.UNSET:
            if os.path.exists(self.addr):
                os.remove(self.addr)
            open(self.addr, "w+")
            try:
                self.sock.serve_forever()
                self._set_server_status(ON)
            except socket.error as msg:
                log.error("failed to open server: %s. Current serverstatus: ", msg, self.get_server_status())
            self._set_server_status(ERROR)
        else:
            log.error("failed to open server, server already running. Current serverstatus: %s",
                      self.get_server_status())
        return self.get_server_status()

    def close_server(self):
        """
        Sluit alle verbindingen en sluit de server af.
        Returns:
            ServerStatus/Enum: Zodat je kan zien of hij wel goed is afgesloten
        """
        try:
            self.sock.server_close()
            os.remove(self.addr)
            self._set_server_status(OFF)
        except socket.error as msg:
            log.error("Failed to close server: %s. Current serverstatus: ", msg, self.get_server_status())

    def get_server_status(self) -> ServerStatus:
        """
        Returns:
            ServerStatus/Enum: Krijg de status van de server (UNSET, ERROR, OFF, ON)
        """
        return self._serverStatus

    def _set_server_status(self, value: ServerStatus) -> ServerStatus:
        """
        Deze functie moet eigenlijk private zijn. Maar omdat dat niet kan met Python zit er een schattig underscortje "_" voor.
        Roep deze methode dan ook absoluut niet aan buiten de Server class!
        Dingen kunnen serieus hard kapot gaan als je dat wel doet.
        Args:
            value (ServerStatus/Emum): de waarde dat de server moet hebben

        Returns:
            ServerStatus/Enum: Zodat je kan kijken of het wel goed hebt gedaan.
        """
        self._serverStatus = self.ServerStatus.value
        return self._serverStatus

    def send(self, param):
        self.send(param)
