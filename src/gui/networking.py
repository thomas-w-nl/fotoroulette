"""
This file includes the networking functionality for the GUI interface.
It is written in GLib's Gio library as to integrate with the signals also
used by GTK.

Copyright (c) 2017-2018, Valentijn van de Beek
"""
import gi
import cv2
import pickle
import json
import threading
import numpy as np

gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gdk
from pathlib import Path
from src.common import log, jsonserializer

class NetworkTask(threading.Thread):
    def __init__(self, callback, message):
        threading.Thread.__init__(self)
        self.callback = callback
        self.message = message
        self.result = None

    def _read_all_bytes(self, input_stream : Gio.IOStream, amount_of_bytes : int=16384) -> bytes:
        """
        A helper function to fetch and collect all the information from the network in one go.

        Args:
           input_stream: The stream with the information in it.
           amount_of_bytes: The amount of bytes it should try to read at the same time. The default is 16384.

        Returns:
           A string with all the information sent through that IO Stream
        """
        acc = bytes()
        result = input_stream.read_bytes(amount_of_bytes, None)

        while result.get_size() != 0:
            acc += result.get_data()  #: Turn GLib bytes into a string
            result = input_stream.read_bytes(amount_of_bytes, None)

        return acc

    def connection_handler(self, client, event, connectable, connection, wtf):
        if event == Gio.SocketClientEvent.CONNECTED:
            output_stream = connection.get_output_stream()
            output_stream.write_all(bytes(self.message, "utf-8"))
            output_stream.flush()

            # todo fix error als input None is
            input_stream = connection.get_input_stream()
            bytes_ = self._read_all_bytes(input_stream)
            response = json.loads(bytes_.decode("utf-8"), object_hook=jsonserializer.from_json)

            if response["message"] == "response":
                self.result = response["result"]

            elif response["message"] == "error":
                log.error("[{0}] {1}".format(response["result"]["code"], response["result"]["message"]))
            else:
                pass

    def run(self):
        server_info = Gio.UnixSocketAddress.new("/tmp/python-processing-ipc")
        connection = Gio.SocketClient()
        connection.connect_after("event", self.connection_handler, connection)
        connection.connect(server_info)

        Gdk.threads_add_idle(100, self.callback, self.result[0] if len(self.result) == 1 else self.result)
