# Scenarios script for testing
import scenarios as sc

if __name__ == "__main__":
    vs = sc.Versus("first game", [
        "assets/taken_pictures/willem.jpeg",
        "assets/taken_pictures/willem.jpeg"
    ])

    vs.generate_image()
