from scenarios.spel import Spel


class Superhelden(Spel):

    def __init__(self, naam, fotos):
        Spel.__init__(self, naam, fotos)

        if len(fotos) != 2:
            raise Exception("length of fotos must be 2")

    def generate_image(self):
        # TODO: generate images and overlay, return generated image path
        return 0

