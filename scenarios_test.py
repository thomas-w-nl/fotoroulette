# Scenarios script for testing
from src import scenarios as sc

if __name__ == "__main__":
    # vs = sc.new_game(sc.Games.VERSUS, "first game", [
    #     "assets/taken_pictures/willem.jpeg",
    #     "assets/taken_pictures/willem.jpeg"
    # ])
    #
    # vs.generate_image()

    # positive is offset in pixels, negative is offset in % from -100 to -1
    # vs = sc.Superheroes("first game", "assets/overlays/superheroes.png")

    vs = sc.Versus("first game", "assets/overlays/versus.png")

    vs.play()
