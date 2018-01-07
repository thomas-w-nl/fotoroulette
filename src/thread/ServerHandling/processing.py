from src.thread.fricp import FRICP
from src.processing.collect_photos import collect_photos
from src.processing.get_faces import get_faces
from src.processing.netwerk import *

class ProcessingHandler:

    @staticmethod
    def handle(fricp: FRICP):
        if fricp.data.request == FRICP.Request.PROCESSING_MAKE_PHOTOS:
            data = collect_photos()

        if fricp.data.request == FRICP.Request.PROCESSING_UPLOAD_NETWORK:
            data = send_photos("fotodata")

        return data
