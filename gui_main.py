import signal
import numpy as np
import subprocess
import os
from multiprocessing import Process
from io import BytesIO
from PIL import Image

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from src.gui import photos
from src.gui.handler import Handler


SOUND = True

def play_sound(file_name: str):
    subprocess.run(["mpv", "--no-resume-playback", "--volume=60", "assets/sound/" + file_name])

class MainWindow:
    """
    The GTK application that displays the photos taken by the photobooth
    """

    def __init__(self):
        """
        Sets up the basic logic of the GTK application
        """
        self._builder = Gtk.Builder()
        self._builder.add_from_file("assets/gui/gui.glade")
        self._builder.connect_signals(Handler(self))

        self._stack = self._builder.get_object("WindowStack")
        self._logo = self._builder.get_object("CorendonLogo")
        self._window = self._builder.get_object("MainWindow")
        self._popup = None  # shitty hack
        self._song = None
        self._photos = photos.PhotoList(self._builder)

        self._set_logo("assets/images/corendon_logo.png", 600, 200)

        # Use CSS for styling
        style = Gtk.CssProvider()
        style.load_from_path("assets/styles/style.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def show_popup(self, popup_name: str) -> Gtk.Dialog:
        """
        Show a popup and disable the screen

        Args:
           popup_name:
        """
        popup = self._builder.get_object(popup_name)
        popup.show_all()
        self._popup = popup
        self._window.set_sensitive(False)

        return popup

    def close_popup(self) -> None:
        """
        Close currently open popup and enable the screen
        """
        if self._popup is not None:
            self._popup.hide()
            self._window.set_sensitive(True)
            self._popup = None

    def _set_logo(self, path: str, width: int, height: int) -> None:
        """
        Sets the logo on top of the application

        Args:
           path: The path to where to logo is
           width: How wide the logo should be
           Height: How high the logo should be
        """
        photo_file = Pixbuf.new_from_file(path)
        photo_scaled = photo_file.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
        self._logo.set_from_pixbuf(photo_scaled)

    def set_photo(self, response: str) -> bool:
        """
        Set the currently showed picture from a string

        Args:
          response: a string containing an (opencv) image
        """
        self._builder.get_object("FidgetSpinner").stop()
        picture_widget = self._builder.get_object("Picture")
        self._stack.set_visible_child_name("picture-view")

        pimage = Image.open(BytesIO(response))
        pimage.save(".temp_image.png")
        image = Pixbuf.new_from_file(".temp_image.png")
        os.remove(".temp_image.png")

        self._photos.append(image)

        picture_widget.set_from_pixbuf(image)
        if self._song_name is not None and SOUND:
            process = Process(target=play_sound, args=(self._song_name,))
            process.start()
            self._song_pid = process.pid

            self._song_process.start()


        self.close_popup()
        return False

    def start(self):
        self._window.show_all()
        self._window.fullscreen()
        Gtk.main()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    window = MainWindow()
    window.start()
