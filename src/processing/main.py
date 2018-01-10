"""
A program that will process images taken by a camera.

Copyright (c) 2017, Valentijn van de Beek
"""
# Import from the parent directory instead
import sys
sys.path.append('..')
sys.path.append('../..')



from common import tools, jsonserializer
from common.log import *
from pathlib import Path
#from processing.collect_photos import collect_photos
#from processing.get_faces import get_faces

import cv2
import json
import pickle
import socketserver
import numpy as np


def send_message(message, address = "/tmp/python-gui-ipc"):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(address)
        sock.sendall(bytes(message + '\n', "utf-8"))
        returned = str(sock.recv(1024, "utf-8"))

    return returned


class IPCHandler(socketserver.StreamRequestHandler):
    def _send_response(self, message):
        self.request.sendall(bytes(json.dumps(message, default=jsonserializer.to_json), "utf-8"))

    def _return_error(self, code : int, message : str) -> None:
        self._send_response({"message": "error", "result": {"code": code, "message": message}})

    def _encode_image(self, file_name : str, encoding : str = '.png') -> str:
        image = cv2.imread(file_name)
        image_string = cv2.imencode(encoding, image)[1].tostring()
        return image_string

    def _send_single_image(self, file_name : str, encoding : str = '.png') -> None:
        self._send_response({"message": "response",
                             "result": [self._encode_image(file_name, encoding)]})

    def handle(self):
        # Fetch the json message
        self.data = self.rfile.readline().decode("utf-8")
        print(self.data)

        message = json.loads(self.data)

        if message["message"] == "command":
            if message["name"] == "get_faces":
                data = collect_photos()
                faces = get_faces(data)
                faces = [face.tostring() for face in faces]
                self._send_response({"message": "response", "result": faces})
            elif message["name"] == "get_image":
                self._send_single_image("/tmp/malloc.png")
            else:
                self._return_error(404, "can't find method '{}'".format(message["name"]))
        elif message["message"] == "play_game":
            if message["name"] == "love_meter":
                self._send_single_image("../../img/cryGirl.jpg")
            elif message["name"] == "versus":
                self._send_single_image("../../img/zombieGirls.jpg")
            elif message["name"] == "superheroes":
                self._send_single_image("../../img/hipsterGirls.jpg")
            elif message["name"] == "mocking":
                self._send_single_image("../../img/rogueGirl.jpg")
        else:
            self._return_error(400, "this server doesn't support '{}'".format(message["message"]))


class IPCServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    pass


if __name__ == "__main__":
    path = Path("/tmp/python-processing-ipc")
    if path.exists():
        path.unlink()

    with IPCServer("/tmp/python-processing-ipc", IPCHandler) as server:
        server.serve_forever()
