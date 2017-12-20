import socket, pickle, cv2
from src.common.log import *
# Client
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
    sock.send(pickle.dump(img))
    # sock.send()

