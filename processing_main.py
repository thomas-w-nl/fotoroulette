"""
A program that will process images taken by a camera.

Copyright (c) 2017, Valentijn van de Beek
"""
# Import from the parent directory instead

import cv2
import json
import socketserver
import numpy as np
from pathlib import Path

from src.common import tools, jsonserializer
from src.common.log import *

from src.processing.get_faces import get_faces
from src.processing.netwerk import send_photos
from src.processing.spel import *
from src.processing.collect_photos import collect_photos
from src.processing.overlay import generate_overlay

# Check whether we're in a raspberry pi or not
try:
    import RPi.GPIO as GPIO
except (ImportError, ModuleNotFoundError):
    print("Running in a fake environment")
    import pickle

    FAKE_ENV = True
    with open('real_2_personen_new.pkl', 'rb') as _file:
        fake_data = pickle.load(_file)
else:
    FAKE_ENV = False

def send_message(message, address = "/tmp/python-gui-ipc"):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(address)
        sock.sendall(bytes(message + '\n', "utf-8"))
        returned = str(sock.recv(1024, "utf-8"))

    return returned


class IPCHandler(socketserver.StreamRequestHandler):
    def __init__(self, request, client_address, server):
        socketserver.StreamRequestHandler.__init__(self, request, client_address, server)
        self.photos = []

    def _send_response(self, message):
        self.request.sendall(bytes(json.dumps(message, default=jsonserializer.to_json), "utf-8"))

    def _return_error(self, code : int, message : str) -> None:
        self._send_response({"message": "error", "result": {"code": code, "message": message}})

    def _encode_image(self, file_ : str, encoding : str = '.png') -> str:
        #image = cv2.imread(file_name)
        image_string = cv2.imencode(encoding, image)[1].tostring()
        return image_string

    def _send_single_image(self, photo, encoding : str = '.png') -> None:
        self._send_response({"message": "response",
                             "result": [cv2.imencode('.png', photo)[1].tostring()]})

    def _start_game(self, game_type):
        if FAKE_ENV:
            data = fake_data
        else:
            data = collect_photos()

        photos_with_angles, range_sensor = data.get()
        faces = get_faces(data)

        log.info("Number of faces found: %s" % len(faces))

        game = (game_by_type(game_type, faces).gen_overlay())
        #self.photos.append(game)
        return game

    def handle(self):
        # Fetch the json message
        self.data = self.rfile.readline().decode("utf-8")
        print(self.data)

        message = json.loads(self.data)

        if message["message"] == "command":
            if message["name"] == "start":
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
                self._send_single_image(self._start_game(Games.LOVEMETER))
            elif message["name"] == "versus":
                self._send_single_image(self._start_game(Games.VERSUS))
            elif message["name"] == "superheroes":
                self._send_single_image(self._start_game(Games.SUPERHEROES))
            elif message["name"] == "wanted":
                self._send_single_image(self._start_game(Games.WANTED))
            else:
                self._send_error(400, "game '%s' not found" % message["message"])
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
