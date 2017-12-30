from src.thread.fricp import FRICP
from src.common.log import *
import src.common.tools as tool

# test client
if __name__ == "__main__":
    log.debug("running in debug mode")
    package = FRICP(request=FRICP.Request.HARDWARE_GET_CAMERA,
                    owner=FRICP.Owner.PROCESSING,
                    address=FRICP.Owner.HARDWARE,
                    buffer_size=1024,
                    open=False)
    try:
        response = FRICP.send(package)
        log.debug("succesvol verzonden en ontvangen YES!")
        tool.draw_image(response.data)
    except FRICP.ValidationError as error:
        response = error.response
        log.debug("dingen gaan mis: %s, err-nr: %s, fricp: %s", error, error.code, error.response.__dict__)
    finally:
        log.debug("response: %s", response.__dict__)


