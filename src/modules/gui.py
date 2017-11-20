import gi
import signal
import cv2
import numpy as np

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk, GObject
from gi.repository.GdkPixbuf import Pixbuf


class PiCamera:
    """
    The camera and related functions
    """
    def __init__(self):
        self._cam = cv2.VideoCapture(-1)
        self._face_cascade = cv2.CascadeClassifier('haarCascades/haarcascade_frontalface_default.xml')

    def get_photo(self):
        """
        Gets the current frame and converts to a GTK readable format

        Returns:
           Raw data readable by Pixbuf
        """
        ret, frame = self._cam.read()

        photo = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = self._face_cascade.detectMultiScale(photo, 1.3, 5)

        for (x, y, w, h) in faces:
            edited = cv2.rectangle(photo, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return photo


class MainWindow:
    """
    The GTK application that displays the photos taken by the photobooth
    """
    def __init__(self, camera):
        """
        Sets up the basic logic of the GTK application

        Args:
           Camera (PiCamera): The connected camera
        """
        self._camera = camera
        self._builder = Gtk.Builder()
        self._builder.add_from_file("gui.glade")
        # self._builder.connect_signals(Handler())

        self._logo = self._builder.get_object("CorendonLogo")
        self._photo = self._builder.get_object("Photo")
        self._window = self._builder.get_object("MainWindow")

        self._set_logo("corendon_logo.png", 800, 150)
        self.get_photo()
        # Below 80 milliseconds causes it to hang
        GObject.timeout_add(80, self.get_photo)

        # Use CSS for styling
        style = Gtk.CssProvider()
        style.load_from_path("style.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    def _set_logo(self, path, width, height):
        """
        Sets the logo on top of the application

        Args:
           path (Str): The path to where to logo is
           width (int): How wide the logo should be
           Height (int): How high the logo should be
        """
        photo_file = Pixbuf.new_from_file(path)
        photo_scaled = photo_file.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
        self._logo.set_from_pixbuf(photo_scaled)

    def get_photo(self):
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

    def start(self):
        self._window.show_all()
        Gtk.main()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    camera = PiCamera()
    window = MainWindow(camera)
    window.start()
