# Scenarios script for testing
import scenarios as sc

if __name__ == "__main__":
    vs = sc.Versus("first game", "assets/data/bg_m.jpg",
                   [
                       ["assets/data/overlay.png", 0, 0],
                       ["assets/data/overlay.png", -1, -1],
                       ["assets/data/overlay.png", -1, 100],

                   ])

    vs.generate_image()
