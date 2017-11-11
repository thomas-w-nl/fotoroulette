class Spel:
    naam = ""
    _fotos = []

    def __init__(self, naam, fotos):
        self.naam = naam
        self._fotos = fotos

    def push_foto(self, foto):
        self._fotos.append(foto)

    def bewerk(self, index):
        return self._fotos[index]

    def clear(self):
        self._fotos = []
