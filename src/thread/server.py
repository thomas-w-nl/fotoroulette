import socket, socketserver, pickle, os
from src.common.log import *
from enum import Enum
from src.thread.fricp import FRICP


class Server:
    class ServerHandeler(socketserver.StreamRequestHandler):
        """
        The RequestHandler class for our server.

        It is instantiated once per connection to the server, and must
        override the handle() method to implement communication to the
        client.
        """

        class ValidationError(Exception):
            def __init__(self, error: FRICP.Response, fricp: FRICP):
                self.error = error
                self.fricp = fricp

            def __str__(self):
                return self.error.name

            def response(self) -> FRICP:
                # TODO: een @property hiervan maken
                # TODO: uitvogelen hoe ik dynamich de owner toekan voegen, het is nu altijd hardware...
                response = FRICP(FRICP.Request.RESPONSE, self.fricp.owner, FRICP.Owner.HARDWARE, self.error)
                return response

        def handle(self):
            # TODO: is data global maken wel handig? Maak er geen gebruik van namelijk
            self.data = pickle.load(self.rfile)
            try:
                self.validate_package(self.data)
            except self.ValidationError as error:
                self.reply(error.response().to_binary())
                log.error("failed to validate incoming fricp package: ", error)
                return -1

        def validate_package(self, fricp: FRICP):
            # TODO: moet validate niet deel zijn van FRICP object?
            # valideren of er geen onbekende waardes inzitten
            if fricp.version is not FRICP.current_version:
                raise self.ValidationError(FRICP.Response.VERSION_MISMATCH, self.data)
            if fricp.request not in FRICP.Request:
                raise self.ValidationError(FRICP.Response.UNKNOWN_REQUEST, self.data)
            if fricp.owner not in FRICP.Owner:
                raise self.ValidationError(FRICP.Response.UNKNOWN_OWNER, self.data)

            # valideren of er geen onmogelijke combinaties inzitten.
            if fricp.request == FRICP.Request.RESPONSE and fricp.response == FRICP.Response.REQUEST:
                raise self.ValidationError(FRICP.Response.INVALID_VALUE_COMBINATION, self.data)

            # Wanneer je data naar jezelf verstuurd
            # TODO: uitzoeken hoe ik erachter kom wie ik ben. Owner is nu HARDWARE
            if fricp.owner == FRICP.Owner.HARDWARE:
                raise self.ValidationError(FRICP.Response.LOOPBACK_DETECTED, self.data)

            # valideren of het request wel uit kan worden gevoert.
            # TODO: owner is nu gehard-coded op HARDWARE. Moet natuurlijk dynamich worden
            if 100 > fricp.request > 199:
                raise self.ValidationError(FRICP.Response.UNABLE_TO_HANDLE_REQUEST, self.data)

        def reply(self, fricp: FRICP):
            self.wfile.write(fricp)

    class ServerStatus(Enum):
        ERROR = -2
        OFF = -1
        ON = 0

    def __init__(self):
        """
        Server class (zit ook de client in). Gebruikt door de hardware; gui en processing om met elkaar te praten door middel van PRICPv1
        Returns:
            Helemaal niks, jonguh BAM!
        """

        # Deze moet je overwriten als je deze class extend
        self.addr = "unixSocket"
        self.owner = FRICP.Owner.invalid_names

        self._serverStatus = self._set_server_status(OFF)
        self.socketServer = socketserver.UnixStreamServer(self.addr, self.ServerHandeler)

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
        if self.get_server_status() < self.ServerStatus.ON:
            if os.path.exists(self.addr):
                os.remove(self.addr)
            open(self.addr, "w+")
            try:
                self.socketServer.serve_forever()
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
            self.socketServer.server_close()
            os.remove(self.addr)
            self._set_server_status(OFF)
        except socket.error as msg:
            log.error("Failed to close server: %s. Current serverstatus: ", msg, self.get_server_status())

    def get_server_status(self) -> ServerStatus:
        """
        Returns:
            ServerStatus/Enum: Krijg de status van de server (UNSET, ERROR, OFF, ON)
        """
        # TODO omzetten naar een @property https://www.programiz.com/python-programming/property
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
        # TODO omzetten naar een @property https://www.programiz.com/python-programming/property
        self._serverStatus = self.ServerStatus.value
        return self._serverStatus

    @staticmethod
    def send(fricp: FRICP) -> FRICP:
        """
        Stuur data volgends het FRICP, raised ook een socket.error als er iets mis gaat
        Args:
            fricp: FRICP object met alle data die je wilt versturen

        Returns:
            FRICP: Het antwoord van de server
        """
        try:
            # TODO: check for open connection
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(fricp.address)
            sock.send(fricp.to_binary())

            # TODO: error handeling
            received = str(sock.recv(fricp.buffer_size), "utf-8")
            received = pickle.load(received)

            if not fricp.open:
                sock.close()

            return received
        except socket.error as msg:
            log.error("Failed to send data: %s.", msg)
            raise socket.error


if __name__ == "__main__":
    log.debug("server running in debug mode")
