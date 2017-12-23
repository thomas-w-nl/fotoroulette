import socket, socketserver, pickle, os, threading
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
                """
                FRICP validation exception object.
                Args:
                    error (FRICP.Response): de error code
                    fricp (FRICP): Het object waar het omgaat
                """
                self.error = error
                self.fricp = fricp

            def __str__(self):
                """
                Returns:
                    String: error-naam
                """
                return self.error.name

            @property
            def code(self):
                """
                Returns:
                    int: error-code
                """
                return self.error.value

            @property
            def response(self) -> FRICP:
                """
                Het correcte response wat je naar de verstuurder moet sturen
                Returns:
                    FRICP: object met de error code en juist addres etc.
                """
                # TODO: Owner word nu bepaald door adres van binnenkomende FRICP, niet heel netjes.
                response = FRICP(FRICP.Request.RESPONSE, self.fricp.address, self.fricp.owner, self.error)
                return response

        def handle(self):
            """
            Standaard functie van socketserver, word automatich geroepen waneer er een request naar de server word gedaan.
            Returns:
                Void
            """
            # TODO: is data global maken wel handig? Maak er geen gebruik van namelijk
            self.data = pickle.load(self.rfile)
            # TODO: owner word nu bepaald door de adres van het binnenkomende fricp pakketjes, dat moet eigenlijk anders
            self.owner = self.data.address
            log.debug("recieved: %s", self.data.__dict__)
            try:
                self.validate_package(self.data)
                log.debug("validation complete, no errors found!")
            except self.ValidationError as error:
                log.error("failed to validate incoming fricp package: %s", error)
                self.reply(error.response)
                return -1
            self.handle_request()

        def handle_request(self):
            """
            Het handelen van de request
            """
            log.debug("handeling request...")
            # TODO: er word eigenlijk niks gehandeled, moet wel.
            # TODO: response is gehardcoded, dat mag natuurlijk helemaal niet.
            response = FRICP(FRICP.Request.RESPONSE, FRICP.Owner.HARDWARE, self.data.owner, FRICP.Response.SUCCESS)
            self.reply(response)

        def validate_package(self, fricp: FRICP):
            """
            Valideren van het binnengekomen FRICP object.
            Er word gecontroleerd op:
                * onbekende waardes
                * onmogelijke combinaties
                * loopback
                * of het request wel kan worden uitgevoerd
            Geeft een ValidationError exception als er iets niet valid is
            Args:
                fricp (FRICP): het object wat moet worden gecontroleerd
            """
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
            # TODO: uitzoeken hoe ik erachter kom wie ik ben. Owner word nu afgeleid van het addres.
            # TODO: hij controleerd nu het pakketjes met zichzelf, dus deze error validatie slaat eigenlijk nergens op
            # TODO: Dit moet bij de Server.send() methode al gecontroleerd worden, niet hier
            if fricp.owner == self.owner:
                raise self.ValidationError(FRICP.Response.LOOPBACK_DETECTED, self.data)

            # valideren of het request wel uit kan worden gevoert.
            if not FRICP.Owner[self.owner.name].min_request_range <= fricp.request.value <= FRICP.Owner[
                self.owner.name].max_request_range:
                raise self.ValidationError(FRICP.Response.UNABLE_TO_HANDLE_REQUEST, self.data)

                # TODO: Er moet eigenlijk ook worden gecontroleerd of de waardes wel deugen (geen data als er wel data word verwacht, request is response bij eerste connectie etc.)

        def reply(self, fricp: FRICP):
            """
            Geef antwoord aan de process die je iets heeft gestuurd.
            Args:
                fricp (FRICP): Het object dat moet worden verstuurd
            """
            log.debug("Sending reply: %s", fricp.__dict__)
            self.wfile.write(fricp.to_binary)

    class ServerStatus(Enum):
        ERROR = -2
        OFF = -1
        ON = 0

    def __init__(self, owner: FRICP.Owner):
        """
        Server class (zit ook de client in). Gebruikt door de hardware; gui en processing om met elkaar te praten door middel van PRICPv1
        Returns:
            Helemaal niks, jonguh BAM!
        """

        # Deze moet je overwriten als je deze class extend
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
                # log.debug("%s, path exists. Removing.", self.server_address)
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
        except socket.error as msg:
            # TODO: geeft dit ding wel een socket.error als het mis gaat? Is het geen OSError?
            log.error("Failed to close server: %s. Current serverstatus: %s", msg, self.server_status.name)
        finally:
            return self.server_status

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
        Roep deze methode dan ook absoluut niet aan buiten de Server class!
        Dingen kunnen serieus hard kapot gaan als je dat wel doet.
        Args:
            value (ServerStatus/Emum): de waarde dat de server moet hebben
        """
        self._serverStatus = value

    @staticmethod
    def send(fricp: FRICP) -> FRICP:
        """
        Stuur data volgends het FRICP, raised ook een socket.error als er iets mis gaat
        Args:
            fricp: FRICP object met alle data die je wilt versturen

        Returns:
            FRICP: Het antwoord van de server
        """
        # TODO: Is het handiger als deze deel is van het FRICP object?
        try:
            # TODO: check for open connection
            log.debug("sending: %s", fricp.__dict__)
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(fricp.address.address)
            sock.send(fricp.to_binary)

            # TODO: error handeling
            received = sock.recv(fricp.buffer_size)
            received = pickle.loads(received)
            log.debug("recieved: %s", received.__dict__)
            if not fricp.open:
                sock.close()

            return received
        except socket.error as msg:
            log.error("Failed to send data: %s.", msg)
            # raise socket.error


if __name__ == "__main__":
    log.debug("server running in debug mode")
