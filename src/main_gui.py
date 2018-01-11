import gi
import signal
import cv2
import numpy as np

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk, GObject
from gi.repository.GdkPixbuf import Pixbuf
from gui import networking

class PiCamera:
    """
    The camera and related functions
    """
    def __init__(self):
        self._cam = cv2.VideoCapture(-1)
        self._face_cascade = cv2.CascadeClassifier('../hairCascade/haarcascade_frontalface_default.xml')

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
        self._builder.add_from_file("gui/new_gui.glade")
        self._builder.connect_signals(Handler(self))

        self._stack = self._builder.get_object("WindowStack")
        self._logo = self._builder.get_object("CorendonLogo")
        #self._photo = self._builder.get_object("Photo")
        self._window = self._builder.get_object("MainWindow")
        self._popup = None # shitty hack

        self._set_logo("../img/corendon_logo.png", 400, 150)
        #self.get_photo()
        # Below 80 milliseconds causes it to hang
        #GObject.timeout_add(80, self.get_photo)

        # Use CSS for styling
        style = Gtk.CssProvider()
        style.load_from_path("../assets/styles/style.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def show_popup(self, popup_name):
        popup = self._builder.get_object(popup_name)
        popup.show_all()
        self._popup = popup
        self._window.set_sensitive(False)

        return popup

    def close_popup(self):
        if self._popup is not None:
            self._popup.hide()
            self._window.set_sensitive(True)
            self._popup = None

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

    def set_photo(self, response):
        picture_widget = self._builder.get_object("Picture")
        self._stack.set_visible_child_name("picture-view")

        nparr = np.fromstring(response, np.uint8)
        print("Shape of the array from string" +str(nparr.shape))

        image_cv2 = cv2.imdecode(nparr, 1)

        print("Shape of the decoded image from string" + str(image_cv2.shape))


        # image_cv2 = cv2.resize(image_cv2, (800, 450))

        print("updating transferred by network image")
        path = "transferred_by_network.png"
        cv2.imwrite("transferred_by_network.png", image_cv2)

        image = Pixbuf.new_from_file(path)
        # photo_scaled = photo_file.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)

        picture_widget.set_from_pixbuf(image)
        self.close_popup()
        return True


    def start(self):
        self._window.show_all()
        Gtk.main()

class Handler:
    def __init__(self, window):
        self.window = window

    def on_start_clicked(self, button):
        self.window._stack.set_visible_child_name("game-menu")

    def on_quit_clicked(self, *args):
        self.window._stack.set_visible_child_name("splash-screen")
        def callback(self, response):
            self._builder.get_object("unique-code").set_text(response)

    def on_save_clicked(self, *args):
        def callback(response):
            self.window._builder.get_object("unique-code").set_text(response)
            self.window._stack.set_visible_child_name("save-screen")
            self.window.close_popup()
            return True

        networking.send_message("{\"message\": \"command\", \"name\": \"send_photos\"}\n", callback)

    def open_save_window(self, *args):
        self.window.show_popup("InformationDialog")

    def on_dialog_close(self, *args):
        print("closed")

    def on_information_clicked(self, button):
        self.window.show_popup("InformationDialog")

    def play_game_pressed(self, button):
        name = self.window._builder.get_object("GameTitle").get_text().lower().replace(' ', '_')
        json_message = "{\"message\": \"play_game\", \"name\": \"%s\"}\n" % name
        networking.send_message(json_message, self.window.set_photo)

    def _show_game_popup(self, name : str, description : str, example_image : str) -> Gtk.Window:
        popup = self.window.show_popup("GameDialog")
        image = Pixbuf.new_from_file(example_image)\
                      .scale_simple(800, 450, GdkPixbuf.InterpType.BILINEAR)
        self.window._builder.get_object("GameTitle").set_text(name)
        self.window._builder.get_object("GameDescription").set_text(description)
        self.window._builder.get_object("GameImage").set_from_pixbuf(image)
        return popup

    def on_superheroes_pressed(self, button):
        self._show_game_popup("Superheroes", "Superheroes", "../img/heroes.svg")

    def on_versus_pressed(self, button):
        self._show_game_popup("Versus", "Versus", "../img/love.svg")

    def on_lovemeter_pressed(self, button):
        self._show_game_popup("Love Meter", "Love Meter", "../img/versus.svg")

    def on_mocking_pressed(self, button):
        self._show_game_popup("Wanted", "Love Meter", "../img/love.svg")

    def on_close_clicked(self, button):
        self.window.close_popup()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    camera = PiCamera()
    networking.create_server()
    window = MainWindow(camera)
    window.start()
