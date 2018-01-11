import pickle, socket
from enum import Enum
from src.common.log import *


class FRICP:
    # Foto Roulette Internal Communication Protocol

    class ValidationError(Exception):
        def __init__(self, error, fricp):
            """
            FRICP validation exception object.
            Args:
                error (FRICP.Response): de error code
                fricp (FRICP): Het object waar het omgaat
            """
            # error type = FRICP.Response en fricp is type FRICP, Maar op run-time herkend hij dat niet.
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
        def response(self):
            """
            Het correcte response wat je naar de afzender moet sturen
            Returns:
                FRICP: object met de error code en juist addres etc.
            """
            response = FRICP(FRICP.Request.RESPONSE, self.fricp.address, self.fricp.owner, self.error)
            return response

    class Response(Enum):
        """
        Het response van de server, is 0 als het een request is
        """
        REQUEST = 0
        # 100-199 is success range
        SUCCESS = 100

        # 200-299 is de error range
        # 200-209 unknown
        UNKNOWN_ERROR = 200  # unused
        UNKNOWN_OWNER = 201
        UNKNOWN_REQUEST = 202
        UNKNOWN_RESPONSE = 203
        UNKNOWN_HANDLING_ERROR = 204

        #
        REJECTED = 210  # unused
        VERSION_MISMATCH = 211
        INVALID_VALUE_COMBINATION = 212
        LOOPBACK_DETECTED = 213
        UNABLE_TO_HANDLE_REQUEST = 214
        INVALID_DATA = 215
        UNEXPECTED_REQUEST_OR_RESPONSE = 216
        FAILED_TO_RECEIVE = 217  # client error

        # 220-229 connection
        CONNECTION_LOST = 220  # heeft dit wel nut? # TODO: implementeren
        CONNECTION_TIMEOUT = 221  # heeft dit wel nut? # TODO: implementeren
        UNABLE_TO_SEND = 222

        # 300-399 is de opdracht range
        CLOSE_CONNECTION = 301  # unused

    class Request(Enum):
        """
        Wat voor request is het? 0 als het een response is
            int: request nr
            Any: Type data, wat bij de request hoort
        """
        RESPONSE = (0, None)
        # SHUTDOWN = 1 is dit handig?
        # 100-199 hardware
        HARDWARE_GET_CAMERA = (100, None)
        HARDWARE_GET_RANGE_SENSOR_DISTANCE = (101, None)
        HARDWARE_GET_SERVO_POSITION = (102, None)
        HARDWARE_SET_SERVO_POSITION = (103, list)

        # 200-299 processing
        PROCESSING_MAKE_PHOTOS = (200, None)
        PROCESSING_GET_PHOTOS = (201, None)  # unused # TODO: impleneteren
        PROCESSING_UPLOAD_NETWORK = (202, None)

        # 300-399 gui
        def __init__(self, request, data_type):
            self.request = request
            self.data_type = data_type

    class Owner(Enum):
        """
        Het address van de sockets, kan ook vervangen worden door ip, port.
        Samen met de request ranges voor validatie
        """
        HARDWARE = ("hardware_unixSocket", 100, 199)
        PROCESSING = ("processing_unixSocket", 200, 299)
        GUI = ("gui_unixSocket", 300, 399)

        def __init__(self, address, min_request_range, max_request_range):
            self.address = address
            self.min_request_range = min_request_range
            self.max_request_range = max_request_range

        @staticmethod
        def list() -> list():
            """
            Krijg een array met strings met alle mogelijke owners
            Returns:
                array: alle owners
            """
            array = []
            for owner in FRICP.Owner:
                array.append(owner.name)
            return array

    current_version = 1

    def __init__(self, request: Request, owner: Owner, address: Owner, response: Response = Response.REQUEST, data=None,
                 open: bool = False, buffer_size: int = 1024, version: float = 1):
        """
        Foto Roulette Internal Communication Protocol
        Protocol voor de communicatie tussen de processing; hardware en gui
        Args:
            request (Request/Enum): De request of response die je doet.
            owner (Owner/Enum): "HARDWARE/GUI/PROCESSING" Wie het bericht verstuurd
            address (Owner/Enum): "HARDWARE/GUI/PROCESSING" waar moet het naartoe?
            response (:obj: `Response/Enum`, optional): "REQUEST" Voor een request.
            data (Any): De data die je verstuurd.
                Bij een response staat de status van het bericht. Default is "UNDEFINED"
            open (:obj: `bool`, optional): true voor een continuous verbinding. Default is false
            buffer_size (:obj: `int`, optional): Hoegroot de buffer moet zijn. Default is 1024
            version (:obj: `float`, optional): De FRICP versie nummer. Default is 1

        Returns:
            object:
        """
        self.request = request
        self.owner = owner
        self.address = address
        self.response = response
        self.data = data
        self.open = open
        self.buffer_size = buffer_size
        self.version = version

        # Misschien is dit handig? Maar nog niet nodig gehad, dus nog niet geimplemteerd
        # self.binaryData =

    def __del__(self):
        """
        Destructor, doet nog niks.
        """
        pass

    @property
    def to_binary(self):
        """
        Returns:
            binary: Krijg het object in een pickle pakketje zodat je het kan versturen
        """
        return pickle.dumps(self)

    @staticmethod
    def validate(fricp, expected: str):
        """
        Valideren van het binnengekomen FRICP object.
        Er word gecontroleerd op:
            * onbekende waardes
            * onmogelijke combinaties
            * loopback
            * of het request wel kan worden uitgevoerd
            * correcte data
            * request/response controleren
        Geeft een ValidationError exception als er iets niet valid is
        Args:
            fricp (FRICP): het object wat moet worden gecontroleerd
            expected (String): "REQUEST" of "RESPONSE", wat je verwacht wat voor paketje het is
        """
        # fricp type is FRICP, maar op run-time geeft hij een error dat hij niet defined is.
        # valideren of er geen onbekende waardes inzitten
        if fricp.version is not FRICP.current_version:
            raise FRICP.ValidationError(FRICP.Response.VERSION_MISMATCH, fricp)
        if fricp.request not in FRICP.Request:
            raise FRICP.ValidationError(FRICP.Response.UNKNOWN_REQUEST, fricp)
        if fricp.owner not in FRICP.Owner:
            raise FRICP.ValidationError(FRICP.Response.UNKNOWN_OWNER, fricp)
        if fricp.response not in FRICP.Response:
            raise FRICP.ValidationError(FRICP.Response.UNKNOWN_RESPONSE, fricp)

        # valideren of er geen onmogelijke combinaties inzitten.
        if fricp.request == FRICP.Request.RESPONSE and fricp.response == FRICP.Response.REQUEST:
            raise FRICP.ValidationError(FRICP.Response.INVALID_VALUE_COMBINATION, fricp)

        # Wanneer je data naar jezelf verstuurd
        if fricp.owner == fricp.address:
            raise FRICP.ValidationError(FRICP.Response.LOOPBACK_DETECTED, fricp)

        # valideren of het request wel uit kan worden gevoert.
        if not FRICP.Owner[fricp.address.name].min_request_range <= fricp.request.request <= FRICP.Owner[
            fricp.address.name].max_request_range and expected == "REQUEST":
            raise FRICP.ValidationError(FRICP.Response.UNABLE_TO_HANDLE_REQUEST, fricp)

        log.debug(type(fricp.data))

        # check of er data moet zijn
        # "None" Moet anders worden gecontroleerd, anders controleerd hij NoneType met None, en daar komt dan false uit.
        required_data_type = FRICP.Request[fricp.request.name].data_type
        data_received_type = fricp.data if required_data_type is None else type(fricp.data)
        if data_received_type is not required_data_type and expected is not "RESPONSE":
            raise FRICP.ValidationError(FRICP.Response.INVALID_DATA, fricp)

        # als je een request verwacht maar een response krijg en visa versa
        if (fricp.request == FRICP.Request.RESPONSE and expected == "REQUEST") or (
                fricp.response == FRICP.Response.REQUEST and expected == "RESPONSE") or (
                fricp.response is not FRICP.Response.REQUEST and expected == "REQUEST"
        ):
            raise FRICP.ValidationError(FRICP.Response.UNEXPECTED_REQUEST_OR_RESPONSE, fricp)

    def send(self):
        """
        Stuur data volgends het FRICP, raised ook een FRICP.ValidationError als er iets mis gaat
        Returns:
            FRICP: Het antwoord van de server
        """
        # Verbinding maken en data versturen
        try:
            # TODO: check for open connection
            log.debug("sending: %s", self.__dict__)
            # TODO: makkelijk kunnen switchen tussen unix socket en ip/poort
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(self.address.address)
            sock.sendall(self.to_binary)
        except socket.error as error:
            log.error("Failed to send data: %s.", error)
            sock.close()
            raise FRICP.ValidationError(FRICP.Response.UNABLE_TO_SEND, self)

        # data ontvangen en uitpakken
        try:
            received = bytearray()
            while True:
                incoming = sock.recv(self.buffer_size)
                received += incoming
                # log.debug(incoming)
                if not incoming:
                    break
            received = pickle.loads(received)
            log.debug("recieved: %s", received.__dict__)
        except (EOFError, pickle.UnpicklingError) as error:
            log.error("Failed to receive data: %s", error)
            # controleren of we wel een bruikbare object hebben ontvangen
            if type(received) is not FRICP:
                received = self
            sock.close()
            raise FRICP.ValidationError(FRICP.Response.FAILED_TO_RECEIVE, received)

        # ontvangen data valideren
        try:
            FRICP.validate(received, "RESPONSE")
            log.debug("validation complete, no errors found!")
        except FRICP.ValidationError as error:
            log.error("failed to validate package: %s", error)
            sock.close()
            raise FRICP.ValidationError(error.error, error.fricp)

        # controleren of de server wel normaal antwoord geeft
        if received.response is not FRICP.Response.SUCCESS:
            log.error("Server responded with error: %s", received.response.name)
            sock.close()
            raise FRICP.ValidationError(received.response, received)

        # sluit de verbinding als dat wenselijk is.
        if (not self.open or received.Response is FRICP.Response.CLOSE_CONNECTION) and not received.open:
            sock.close()

        # als alles welletjes is gegaan geef dan het response terug
        return received
