from src.thread.server import Server
from src.thread.fricp import FRICP
from src.processing.collect_photos import collect_photos
from src.processing.get_faces import get_faces # unused # TODO: uitzoeken of dit nog nutig is
from src.processing.netwerk import *
from src.common.log import *

# TODO: code testen
# TODO: documentatie

def handle(fricp: FRICP):
    try:
        if fricp.data.request == FRICP.Request.PROCESSING_MAKE_PHOTOS:
            data = collect_photos()

        if fricp.data.request == FRICP.Request.PROCESSING_UPLOAD_NETWORK:
            data = send_photos("fotodata")
    except Exception as error:
        log.error("Error while handeling request: %s", error)
        raise FRICP.ValidationError(FRICP.Response.UNKNOWN_HANDLING_ERROR, fricp)
    return data