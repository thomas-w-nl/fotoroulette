import qrcode
import os
import threading

import gi
import threading
import signal
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf, Gdk, GObject, GLib
from gi.repository.GdkPixbuf import Pixbuf
from src.gui.networking import NetworkTask
from src.common.log import *

GObject.threads_init()

class Handler:
    def __init__(self, window):
        self.window = window

    def _game_menu_error(self, error_message: str) -> bool:
        self.window._builder.get_object("FidgetSpinner").stop()
        self.window.close_popup()
        self.window._stack.set_visible_child_name("game-menu")
        error_bar = self.window._builder.get_object("GameMenuError")
        error_bar.set_text(error_message)
        error_bar.set_sensitive(True)

        GLib.timeout_add_seconds(10, lambda: error_bar.set_sensitive(False))

    def on_start_clicked(self, button):
        self.window._stack.set_visible_child_name("game-menu")

    def on_pick_game_clicked(self, *args):
        self.window._stack.set_visible_child_name("game-menu")
        os.kill(self.window._song_pid + 1, signal.SIGKILL)

    def on_back_clicked(self, *args):
        self.window._stack.set_visible_child_name("game-menu")
        self.window._photos.to_start()

    def on_quit_clicked(self, *args):
        self.window._stack.set_visible_child_name("splash-screen")
        self.window._photos.clear()

        def callback(self, response):
            self._builder.get_object("unique-code").set_text(response)

    def on_preview_clicked(self, *args):
        photos = self.window._photos

        if photos.is_empty():
            self._game_menu_error("[403]: Geen gezichten opgeslagen")
            return

        photos._show_arrows()
        self.window._builder.get_object("PreviewPicture").set_from_pixbuf(photos.get_current_photo())
        self.window._stack.set_visible_child_name("preview-photos")
        self.window._builder.get_object("LeftArrow").hide()

    def on_left_clicked(self, *args):
        photos = self.window._photos

        try:
            self.window._builder.get_object("PreviewPicture").set_from_pixbuf(photos.previous_photo())
        except IndexError:
            log.error("Error")

        return True

    def on_right_clicked(self, *args):
        photos = self.window._photos

        try:
            self.window._builder.get_object("PreviewPicture").set_from_pixbuf(photos.next_photo())
        except IndexError:
            pass

        return True


    def on_save_clicked(self, *args):
        def callback(response):
            self.window._builder.get_object("FidgetSpinner").stop()
            self.window._builder.get_object("unique-code").set_text(response)
            self.window._stack.set_visible_child_name("save-screen")

            photo = qrcode.make("https://fys.1hz.nl/nl/pictures/%s" % response)
            photo = photo.get_image().resize((200, 200))
            photo.save("qr-code.png", "PNG")

            image = Pixbuf.new_from_file("qr-code.png")
            self.window._builder.get_object("qr-code").set_from_pixbuf(image)
            os.remove("qr-code.png")

            return False

        if self.window._photos.is_empty():
            self._game_menu_error("[403]: Geen gezichten opgeslagen")
            return

        self.window._stack.set_visible_child_name("photo-wait")
        self.window._builder.get_object("FidgetSpinner").start()
        self.window.close_popup()

        NetworkTask(callback,
                    self._game_menu_error,
                    "{\"message\": \"command\", \"name\": \"send_photos\"}\n").start()

    def open_save_window(self, *args):
        self.window.show_popup("StopGameDialog")

    def on_information_clicked(self, button):
        self.window.show_popup("InfoDialog")

    def play_game_pressed(self, button):
        # Enable the waiting screen
        self.window._stack.set_visible_child_name("photo-wait")
        self.window._builder.get_object("FidgetSpinner").start()
        self.window.close_popup()

        # We need to simplify the name to something we can send over the network
        name = self.window._builder.get_object("GameTitle").get_text().lower().replace(' ', '_')
        json_message = "{\"message\": \"play_game\", \"name\": \"%s\"}\n" % name

        # Send it over the network in a thread
        thread = NetworkTask(self.window.set_photo,
                             self._game_menu_error,
                             json_message)
        thread.start()

    def _show_game_popup(self, name: str, description: str, example_image: str, song: str) -> Gtk.Window:
        self.window._song_name = song

        popup = self.window.show_popup("GameDialog")
        image = Pixbuf.new_from_file(example_image)
        self.window._builder.get_object("GameTitle").set_text(name)
        self.window._builder.get_object("GameDescription").set_text(description)
        self.window._builder.get_object("GameImage").set_from_pixbuf(image)
        return popup

    def on_superheroes_pressed(self, button):
        self._show_game_popup("Superheroes",
                              "Iedereen wilt wel een superheld zijn maar lang niet iedereen is daar geschikt voor. Superheroes analyseert de vaardigheden van iedere speler en vergelijkt deze met bekende helden als Superman en Batman. De uiteindelijk geselecteerde spelers worden aan het publiek getoont d.m.v een poster die overal te zien zal zijn.",
                              "assets/images/superheroes-example.jpg", "heroes.mp3")

    def on_versus_pressed(self, button):
        self._show_game_popup("Versus",
                              "Bij versus draait het erom dat de wedstrijd gelijk is maar dat de rivaliteit extreem hoog ligt."
                              "De meest rivaliserende spelers komen oog in oog te staan met elkaar waarna het ultieme gevecht zal beginnen.",
                              "assets/images/versus-example.jpg", "fatality.mp3")

    def on_lovemeter_pressed(self, button):
        self._show_game_popup("Love Meter",
                              "De Lovemeter selecteert twee spelers om zo het perfecte koppel samen te stellen."
                              "Denkt u dat u op het punt de ware liefde te gaan vinden maar u wilt het 100% weten, speel dan de Lovemeter!",
                              "assets/images/love-example.jpg", "dingDong.mp3")

    def on_mocking_pressed(self, button):
        self._show_game_popup("Wanted",
                              "Wanted checkt de achtergrond van de spelers om vervolgens de meest criminele speler bekend te maken d.m.v een “wanted”-poster.",
                              "assets/images/wanted-example.jpg", "finishHim.mp3")

    def on_close_clicked(self, button):
        self.window.close_popup()
1
