import socket, os, socketserver, pickle, sys, threading
from src.common.log import *
from enum import Enum
from src.thread.fricp import FRICP
from src.thread import hardware_handle as hardware, processing_handle as processing


class Server:
    class ServerHandeler(socketserver.StreamRequestHandler):
        """
        The RequestHandler class for our server.

        It is instantiated once per connection to the server, and must
        override the handle() method to implement communication to the
        client.
        """

        def handle(self):
            """
            Standaard functie van socketserver, word automatich geroepen
            waneer er een request naar de server word gedaan.

            Returns:
                Void

            """
            try:
                log.debug("Incoming package")
                self.data = FRICP.build(self.rfile)
                log.debug("recieved: %s", self.data.__dict__)
                FRICP.validate(self.data, "REQUEST")
                log.debug("validation complete, no errors found!")
            except FRICP.ValidationError as error:
                log.error("failed to validate incoming fricp package: %s", error)
                self.reply(error.response)
                return -1
            self.handle_request()

        def handle_request(self):
            """
            Het handelen van de request
            """
            log.debug("handeling request...")

            try:
                if self.data.address == FRICP.Owner.HARDWARE:
                    response_data = hardware.handle(self.data)

                if self.data.address == FRICP.Owner.PROCESSING:
                    response_data = processing.handle(self.data)

                if self.data.address == FRICP.Owner.GUI:
                    # TODO: GUI handeler met FRICP
                    raise FRICP.ValidationError(FRICP.Response.UNABLE_TO_HANDLE_REQUEST, self.data)

                response = FRICP(FRICP.Request.RESPONSE, self.data.address, self.data.owner, FRICP.Response.SUCCESS,
                                 response_data,
                                 buffer_size=self.data.buffer_size)
            except FRICP.ValidationError as error:
                log.error("Error while handeling request: %s", error)
                response = error.response
            self.reply(response)

        def reply(self, fricp: FRICP):
            """
            Geef antwoord aan de process die je iets heeft gestuurd.

            Args:
                fricp (FRICP): Het object dat moet worden verstuurd
            """
            log.debug("Sending reply: %s", fricp.__dict__)
            # self.request.sendall(fricp.to_binary)
            self.wfile.write(fricp.to_binary)

    class ServerStatus(Enum):
        ERROR = -2
        OFF = -1
        ON = 0

    def __init__(self, owner: FRICP.Owner):
        """
        Server class. Gebruikt door de hardware; gui en processing om met elkaar
        te praten door middel van PRICPv1

        Returns:
            Helemaal niks, jonguh BAM!
        """

        # TODO: eigenlijk moet er ook een flag staan of het een socketserver of TCP/IP address is zodat je ook over internet dingen kan sturen. Unix socket is nu gehardcoded
        self.owner = owner
        self.server_address = owner.address
        self._serverStatus = self.server_status = self.ServerStatus.OFF
        self.socketServer = None

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
        if self.server_status is not self.ServerStatus.ON:
            if os.path.exists(self.server_address):
                log.debug("%s, path exists. Removing.", self.server_address)
                os.remove(self.server_address)
            try:
                self.socketServer = socketserver.UnixStreamServer(self.server_address, self.ServerHandeler)

                # Start the server in een thread zodat de code daarna nogsteeds word uitgevoerd.
                threading.Thread(target=self.socketServer.serve_forever).start()
                self.server_status = self.ServerStatus.ON
                log.debug("Running %s server", self.owner.name)
            except OSError as error:
                log.error("failed to open server, OSError: %s. Current serverstatus: %s", error.strerror,
                          self.server_status.name)
                self.server_status = self.ServerStatus.ERROR
            except socket.error as msg:
                # TODO: Kan deze exception wel voorkomen of doet socketserver alleen OSError?
                log.error("failed to open server, socketError: %s. Current serverstatus: %s", msg,
                          self.server_status.name)
                self.server_status = self.ServerStatus.ERROR
        else:
            log.error("failed to open server, server already running. Current serverstatus: %s",
                      self.server_status.name)

        if self.owner == FRICP.Owner.HARDWARE:
            hardware.init()

        return self.server_status

    def close_server(self):
        """
        Sluit alle verbindingen en sluit de server af.

        Returns:
            ServerStatus/Enum: Zodat je kan zien of hij wel goed is afgesloten
        """
        try:
            self.socketServer.server_close()
            os.remove(self.server_address)
            self.server_status = self.ServerStatus.OFF

            if self.owner == FRICP.Owner.HARDWARE:
                hardware.delete()

        except socket.error as msg:
            # TODO: geeft dit ding wel een socket.error als het mis gaat? Is het geen OSError?
            log.error("Failed to close server: %s. Current serverstatus: %s", msg, self.server_status.name)
        finally:
            return self.server_status

    # TODO: close_server() moet eigenlijk vervangen worden door server_status
    @property
    def server_status(self) -> ServerStatus:
        """
        Returns:
            ServerStatus/Enum: Krijg de status van de server (UNSET, ERROR, OFF, ON)
        """
        return self._serverStatus

    @server_status.setter
    def server_status(self, value: ServerStatus):
        """
        Deze functie moet eigenlijk private zijn.
        schakelt ook de server uit, als je hem op off zet. Om zombie processen tegen te gaan.
        Het is nog steeds niet de bedoeling dat je deze setter gebruikt

        Args:
            value (ServerStatus/Emum): de waarde dat de server moet hebben
        """
        self._serverStatus = value
        # Server uitzetten zodat je geen zombie processen kan krijgen
        if value == self.ServerStatus.OFF:
            self.close_server()


if __name__ == "__main__":
    log.debug("server running in debug mode")
