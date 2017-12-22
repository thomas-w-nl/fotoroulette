import pickle
from enum import Enum


class FRICP:
    # Foto Roulette Internal Communication Protocol

    class Response(Enum):
        REQUEST = 0
        # 100-199 is success range
        SUCCESS = 100

        # 200-299 is de error range
        # 200-209 unknown
        UNKNOWN_ERROR = 200
        UNKNOWN_OWNER = 201
        UNKNOWN_REQUEST = 202
        UNKNOWN_RESPONSE = 203  # heeft dit wel nut?

        #
        REJECTED = 210
        VERSION_MISMATCH = 211
        INVALID_VALUE_COMBINATION = 212
        LOOPBACK_DETECTED = 213
        UNABLE_TO_HANDLE_REQUEST = 214

        # 220-229 connection
        CONNECTION_LOST = 220  # heeft dit wel nut?
        CONNECTION_TIMEOUT = 221  # heeft dit wel nut?

        # 300-399 is de opdracht range
        CLOSE_CONNECTION = 301

    class Request(Enum):
        RESPONSE = 0
        # 100-199 hardware
        HARDWARE_GET_CAMERA = 100
        HARDWARE_GET_RANGE_SENSOR = 101
        HARDWARE_GET_SERVO_POSITION = 102
        HARDWARE_POST_SERVO_POSITION = 103

        # 200-299 processing

        # 300-399 gui


    class Owner(Enum):
        HARDWARE = 1
        PROCESSING = 2
        GUI = 3

    current_version = 1

    def __init__(self, request: Request, owner: Owner, address: Owner, response: Response = Response.REQUEST, data=None,
                 open: bool = false, buffer_size: int = 1024, version: float = 1):
        """
        Foto Roulette Internal Communication Protocol
        Protocol voor de communicatie tussen de processing; hardware en gui
        Args:
            request (Request/Enum): De request of response die je doet.
            owner (Owner/Enum): "HARDWARE/GUI/PROCESSING" Wie het bericht verstuurd
            address (Owner/Enum): "HARDWARE/GUI/PROCESSING" waar moet het naartoe?
            response (:obj: `Response/Enum`, optional): "UNDEFINED" Voor een request.
            data (Any): De data die je verstuurd.
                Bij een response staat de status van het bericht. Default is "UNDEFINED"
            open (:obj: `bool`, optional): true voor een continuous verbinding. Default is false
            buffer_size (:obj: `int`, optional): Hoegroot de buffer moet zijn. Default is 1024
            version (:obj: `float`, optional): De FRICP versie nummer. Default is 1
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
        pass

    def to_dictionary(self):
        """
        Krijg de directionary van het fricp object met alle data. Zodat je er wat nuttige dingen mee kan doen.
        Returns:
            dictionary: Dirtionary van het FRICP

        """
        # TODO: een @property hiervan maken
        # TODO: testen of __dict__ niet gewoon hetzelfde doet.
        # TODO: Strip address
        return {'request': self.request, 'owner': self.owner, 'address': self.address, 'response': self.response,
                'data': self.data, 'open': self.open, 'buffer_size': self.buffer_size, 'version': self.version}

    def to_binary(self):
        """
        Returns:
            binary: Krijg de dirtionary in een pickle pakketje zodat je het kan versturen
        """
        # TODO: een @property hiervan maken
        return pickle.dumps(self.to_dictionary())
