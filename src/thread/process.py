
import socket
import cv2
from src.common.log import *

addres = "unix_socket"
myString = "hello world"
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    sock.connect(addres)
    sock.send(myString.encode())
    received = str(sock.recv(1024), "utf-8")
    log.debug(received)
except socket.error as msg:
    log.error("server failed: %s", msg)


if __name__ == "__main__":
    log.debug("module running as main!")
    import src.common.tools as tool
    img = tool.get_image("img/ardnold.jpg")
    log.debug(type(img))
    cv2.imencode('.jpg', img)
    log.debug(type(img))

    # sock.send()
