from src.thread.fricp import FRICP
from src.common.log import *

# test client
if __name__ == "__main__":
    log.debug("running in debug mode")
    package = FRICP(request=FRICP.Request.HARDWARE_GET_CAMERA,
                    owner=FRICP.Owner.HARDWARE,
                    address=FRICP.Owner.PROCESSING)
    try:
        response = FRICP.send(package)
        log.debug("succesvol verzonden en ontvangen YES!")
    except FRICP.ValidationError as error:
        response = error.response
        log.debug("dingen gaan mis: %s, err-nr: %s, fricp: %s", error, error.code, error.response.__dict__)
    finally:
        log.debug("response: %s", response.__dict__)
