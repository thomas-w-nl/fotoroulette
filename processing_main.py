#
# A program that will process images taken by a camera.
#
# Copyright (c) 2017, Valentijn van de Beek
#
# Import from the parent directory instead

import random
import json
import socketserver
import numpy as np

from PIL import Image
from time import sleep
from pathlib import Path
from io import BytesIO

from src.common import tools, jsonserializer
from src.common.log import *

from src.processing.get_faces import get_faces
from src.processing.netwerk import send_photos_by_path, UploadException
from src.processing.spel import *
from src.processing.collect_photos import collect_photos
from src.processing.overlay import generate_overlay

# Check whether we're in a raspberry pi or not
try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Running in a fake environment")
    print("This is very dangerous regarding to errors. Please debug using ImportError and ModuleNotFound exeptions")
    import pickle

    FAKE_ENV = True
    with open('real_2_personen_new.pkl', 'rb') as _file:
        fake_data = pickle.load(_file)
else:
    FAKE_ENV = False


def send_message(message : str, address = "/tmp/python-gui-ipc") -> str:
    """
    Send a message to a specified UNIX socket, generally the GUI.

    Args:
       message: The message you want to send
       address: The path to the UNIX socket
    """
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(address)
        sock.sendall(bytes(message + '\n', "utf-8"))
        returned = str(sock.recv(1024, "utf-8"))

    return returned


class IPCHandler(socketserver.StreamRequestHandler):
    photos = []

    def _send_response(self, message : str) -> None:
        """
        Send back a response over the network.

        Args:
           message: a string containing a json message
        """
        self.request.sendall(bytes(json.dumps(message, default=jsonserializer.to_json), "utf-8"))

    def _send_error(self, code: int, message: str) -> None:
        """
        Send back an error message as a response.

        Args:
           code: The error code specifying what happened.
           message: A message describing what happened.
        """
        self._send_response({"message": "error", "result": {"code": code, "message": message}})

    def _send_single_image(self, photo : Image, encoding: str = '.png') -> None:
        """
        Send a single image as response

        Args:
          photo: A Pillow picture you want to send
          encoding: the type of picture you want to send, by default png
        """
        log.debug("Sending a single image of type:" + str(type(photo)))
        photo_string = BytesIO()
        photo.save(photo_string, format="PNG")
        self._send_response({"message": "response", "result": [photo_string.getvalue()]})

    def _start_game(self, game_type) -> None:
        """ Play the specified game and send the picture or an error to the back"""
        if FAKE_ENV:
            data = fake_data
        else:
            data = collect_photos()

        faces = get_faces(data, game_type)

        log.info("Number of faces found: %s" % len(faces))

        try:
            game = (game_by_type(game_type, faces).gen_overlay())
            self.photos.append(game)
        except ValueError as err:
            log.warning("Not enough players to create overlay")
            self._send_error(502, "Not enough faces to generate an overlay")
        else:
            self._send_single_image(game)

    def handle(self):
        # Fetch the json message
        self.data = self.rfile.readline().decode("utf-8")

        print(self.data)

        message = json.loads(self.data)

        if message["message"] == "command":
            if message["name"] == "start":
                self.photos = []
            elif message["name"] == "get_image":
                self._send_single_image("/tmp/malloc.png")
            elif message["name"] == "send_photos":
                # todo gebruik cv2.imgencode
                # Due to the backend implementation we first need to write the photos to disk
                directory_name = "/tmp/vakantieklieker-fotos-" + str(random.randint(0, 10000))
                path = Path(directory_name)
                path.mkdir()

                for photo_index in range(len(self.photos)):
                    self.photos[photo_index].save("{0}/{1}.png".format(directory_name, photo_index))

                response = send_photos_by_path(directory_name)

                # Remove the unneeded directories
                for file_ in path.glob('*'):
                    file_.unlink()
                path.rmdir()

                self.photos.clear()

                self._send_response({"message": "response", "result": [response]})
            else:
                self._send_error(404, "can't find method '{}'".format(message["name"]))

        elif message["message"] == "play_game":
            if message["name"] == "love_meter":
                self._start_game(Games.LOVEMETER)
            elif message["name"] == "versus":
                self._start_game(Games.VERSUS)
            elif message["name"] == "superheroes":
                self._start_game(Games.SUPERHEROES)
            elif message["name"] == "wanted":
                self._start_game(Games.WANTED)
            else:
                self._send_error(400, "game '%s' not found" % message["message"])
        else:
            self._send_error(400, "this server doesn't support '{}'".format(message["message"]))


class IPCServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    pass


if __name__ == "__main__":
    path = Path("/tmp/python-processing-ipc")
    if path.exists():
        path.unlink()
    server = IPCServer("/tmp/python-processing-ipc", IPCHandler)

    server.serve_forever()
    server.shutdown()
