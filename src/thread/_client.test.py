from src.thread.fricp import FRICP
from src.common.log import *
import pickle
import src.common.tools as tool
from src.thread import start as thread_start

# TODO: als alles getest is en werkt, moet deze boi verwijderd worden.

# test client
if __name__ == "__main__":
    log.debug("running in debug mode")
    # log.debug(thread_start(["HARDWARE"]))
    package = FRICP(request=FRICP.Request.HARDWARE_GET_CAMERA,
                    owner=FRICP.Owner.PROCESSING,
                    address=FRICP.Owner.HARDWARE,
                    buffer_size=1024,
                    open=False)

    # log.debug(package._to_array)
    # packed = package.to_binary
    # log.debug(packed)
    # log.debug(FRICP.build(packed).__dict__)

    try:
        response = FRICP.send(package)
        log.debug("succesvol verzonden en ontvangen YES!")
        tool.draw_image(response.data)
    except FRICP.ValidationError as error:
        response = error.response
        log.debug("dingen gaan mis: %s, err-nr: %s", error, error.code)
    finally:
        log.debug("response: %s", response.__dict__)
