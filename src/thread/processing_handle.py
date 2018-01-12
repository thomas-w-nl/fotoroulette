from src.thread.fricp import FRICP
from src.processing.collect_photos import collect_photos
from src.processing.get_faces import get_faces  # unused # TODO: uitzoeken of dit nog nutig is
from src.processing.netwerk import *
from src.common.log import *


# TODO: code testen
# TODO: RP libary errors fixen


def handle(fricp: FRICP) -> object:
    """
    functie om data op te vragen van de processing handeler.
    kan een FRICP.ValidationError exception throwen

    Args:
        fricp(FRICP): het object wat gehandled moet worden

    Returns:
        object: data van het gevraagte object

    """
    try:
        if fricp.data.request == FRICP.Request.PROCESSING_MAKE_PHOTOS:
            data = collect_photos()

        if fricp.data.request == FRICP.Request.PROCESSING_UPLOAD_NETWORK:
            data = send_photos("fotodata")
    except Exception as error:
        log.error("Error while handeling request: %s", error)
        raise FRICP.ValidationError(FRICP.Response.UNKNOWN_HANDLING_ERROR, fricp)
    return data
