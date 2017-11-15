# Scenarios script for testing
import scenarios as sc

if __name__ == "__main__":
    vs = sc.Versus("first game", "assets/data/background.jpg",
                   [
                       ["assets/data/overlay.png", 0, 0],
                       ["assets/data/overlay.png", 100, 30]

                   ])

    vs.generate_image()
