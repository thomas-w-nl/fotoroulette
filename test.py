from src.processing import spel
import cv2

if __name__ == "__main__":
    im = spel.Wanted().gen_overlay()

    cv2.imshow('1', im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
