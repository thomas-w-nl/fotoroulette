class Spel:
    def __init__(self, naam, fotos):
        self.naam = naam
        self._fotos = fotos

    def push_foto(self, foto):
        self._fotos.append(foto)

    def bewerk(self, index):
        return self._fotos[index]

    def clear(self):
        self._fotos = []


class Superhelden(Spel):

    def __init__(self, naam, fotos):
        Spel.__init__(self, naam, fotos)

        if len(fotos) != 2:
            raise Exception("length of fotos must be 2")

    def generate_image(self):
        # TODO: generate images and overlay, return generated image path
        return 0

