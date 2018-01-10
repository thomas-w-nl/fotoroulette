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
import numpy as np

gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio
from pathlib import Path
from common import log, jsonserializer

def _read_all_bytes(input_stream : Gio.IOStream, amount_of_bytes : int=16384):
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


def send_message(message : str, callback, path : str = "/tmp/python-processing-ipc"):
    """
    Send a message to a UNIX socket and receive the output

    Args:
       message: The message you want to send.
       path: The path to the UNIX socket

    Returns:
       None
    """
    def connection_handler(client, event, connectable, connection, wtf):
        if event == Gio.SocketClientEvent.CONNECTED:
            output_stream = connection.get_output_stream()
            output_stream.write_all(bytes(message, "utf-8"))
            output_stream.flush()

            input_stream = connection.get_input_stream()
            bytes_ = _read_all_bytes(input_stream)
            response = json.loads(bytes_.decode("utf-8"), object_hook=jsonserializer.from_json)

            if response["message"] == "response":
                for image in response["result"]:
                    callback(image)

            elif response["message"] == "error":
                print("[{0}] {1}".format(response["result"]["code"], response["result"]["message"]))
            else:
                pass

    server_info = Gio.UnixSocketAddress.new(path)
    connection = Gio.SocketClient()
    connection.connect_after("event", connection_handler, connection)
    connection.connect(server_info)


def create_server(path_name : str = "/tmp/python-gui-ipc"):
    """
    Create a Gio server using a TCP Unix Socket on a specified address

    Args:
       path: The path to the UNIX socket

    """
    def connection_handler(socket_service, connection, source_object, unknown):
        input_stream = connection.get_input_stream()
        print(input_stream.read_bytes(8192, None).get_data())

        output_stream = connection.get_output_stream()
        bytes_written = output_stream.write_all(pickle.dumps(image))
        output_stream.flush()

        connection.close()

    path = Path(path_name)

    if path.exists():
        path.unlink()

    # Some silly test ata
    image = cv2.imread("/tmp/malloc.png")
    server = Gio.SocketService.new()
    server.add_address(Gio.UnixSocketAddress.new(path_name), Gio.SocketType.STREAM, Gio.SocketProtocol.DEFAULT)
    server.connect("incoming", connection_handler, server)


if __name__ == "__main__":

    create_server()
    main = GLib.MainLoop()
    main.run()
