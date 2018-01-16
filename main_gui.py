import gi
import signal
import cv2
import numpy as np

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf, Gdk, GObject
from gi.repository.GdkPixbuf import Pixbuf
from src.gui import networking
from src.gui.handler import Handler
b
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
        self._popup = None # shitty hack

        self._set_logo("img/corendon_logo.png", 400, 150)

        # Use CSS for styling
        style = Gtk.CssProvider()
        style.load_from_path("assets/styles/style.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def show_popup(self, popup_name : str) -> Gtk.Dialog:
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

    def _set_logo(self, path : str, width : int, height : int) -> None:
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

    def get_photo(self) -> bool:
        """Display the current image from the webcam on screen"""
        frame = self._camera.get_photo()
        image = Pixbuf.new_from_data(frame.tostring(),
                                     GdkPixbuf.Colorspace.RGB,
                                     False,
                                     8,
                                     frame.shape[1],
                                     frame.shape[0],
                                     frame.shape[2] * frame.shape[1])
        self._photo.set_from_pixbuf(image)
        # Maakt GTK blij
        return True

    def set_photo(self, response : str) -> bool:
        """
        Set the currently showed picture from a string

        Args:
          response: a string containing an (opencv) image
        """
        picture_widget = self._builder.get_object("Picture")
        self._stack.set_visible_child_name("picture-view")

        nparr = np.fromstring(response, np.uint8)
        image_cv2 = cv2.imdecode(nparr, 1)

        path = "transferred_by_network.png"
        cv2.imwrite(path, image_cv2)
        image = Pixbuf.new_from_file(path)
        os.remove(path)

        picture_widget.set_from_pixbuf(image)
        self.close_popup()
        return True


    def start(self):
        self._window.show_all()
        Gtk.main()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    networking.create_server()
    window = MainWindow()
    window.start()
