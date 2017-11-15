# Scenarios script for testing
import scenarios as sc

if __name__ == "__main__":
    # positive is offset in pixels, negative is offset in % from -100 to -1
    vs = sc.Versus("first game", "assets/data/background.jpg",
                   [
                       ["assets/data/overlay.png", 0, 0],  # top left corner
                       ["assets/data/overlay.png", 100, 30],  # offset by 100px to the right and 30 down
                       ["assets/data/overlay.png", -33, -33],  # offset by 33% to the right and down

                   ])

    vs.generate_image()
