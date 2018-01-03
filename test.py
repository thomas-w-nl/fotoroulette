from src.processing import spel
import cv2
from src.processing import collect_photos
from src.processing import get_faces


if __name__ == "__main__":
    im = spel.Superheroes(get_faces.get_faces(collect_photos.collect_photos())).gen_overlay()

    cv2.imshow('1', im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
