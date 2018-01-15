class Handler:
    def __init__(self, window):
        self.window = window

    def on_start_clicked(self, button):
        self.window._stack.set_visible_child_name("game-menu")

    def on_quit_clicked(self, *args):
        self.window._stack.set_visible_child_name("splash-screen")
        self.window._photos.clear()

    def on_save_clicked(self, *args):
        def callback(response):
            self.window._builder.get_object("unique-code").set_text(response)
            self.window._stack.set_visible_child_name("save-screen")
            self.window.close_popup()
            print(response)
            return True

        networking.send_message("{\"message\": \"command\", \"name\": \"send_photos\"}\n", callback)

    def open_save_window(self, *args):
        self.window.show_popup("InformationDialog")

    def on_dialog_close(self, *args):
        print("closed")

    def on_information_clicked(self, button):
        self.window.show_popup("InformationDialog")

    def play_game_pressed(self, button):
        # We need to simplify the name to something we can send over the network
        name = self.window._builder.get_object("GameTitle").get_text().lower().replace(' ', '_')
        json_message = "{\"message\": \"play_game\", \"name\": \"%s\"}\n" % name
        networking.send_message(json_message, self.window.set_photo)

    def _show_game_popup(self, name : str, description : str, example_image : str, song : str) -> Gtk.Window:
        self.window._song = song

        popup = self.window.show_popup("GameDialog")
        image = Pixbuf.new_from_file(example_image)\
                      .scale_simple(800, 450, GdkPixbuf.InterpType.BILINEAR)
        self.window._builder.get_object("GameTitle").set_text(name)
        self.window._builder.get_object("GameDescription").set_text(description)
        self.window._builder.get_object("GameImage").set_from_pixbuf(image)
        return popup

    def on_superheroes_pressed(self, button):
        self._show_game_popup("Superheroes", "Superheroes", "assets/images/heroes.svg", "heroes.mp3")

    def on_versus_pressed(self, button):
        self._show_game_popup("Versus", "Versus", "../img/love.svg", "fatality.mp3")

    def on_lovemeter_pressed(self, button):
        self._show_game_popup("Love Meter", "Love Meter", "assets/images/versus.svg", "dingDong.mp3")

    def on_mocking_pressed(self, button):
        self._show_game_popup("Wanted", "Love Meter", "assets/images/love-example.png", "finishHim.mp3")

    def on_close_clicked(self, button):
        self.window.close_popup()
