import requests
import json
import os
import numpy as np


class UploadException(Exception):
    pass

def send_photos(photos: np.array) -> str:
    """
    Verstuur foto's naar server en verkrijg sessionID

    Args:
       photos: De daadwerkelijke foto's die gestuurd worden

    Returns:
       De sessionID die gereturned wordt van de server
    """
    headers = {"auth": "SUPER_GEHEIME_KEY"}

    r = requests.post("https://fys.1hz.nl/api/session/upload",
                      files=photos,
                      headers=headers)
    content = json.loads(r.content.decode('utf8'))

    if content['result'] == "error":
        raise UploadException(content['reason'])

    return content

def send_photos_by_path(image_path : str) -> str:
    """
    Verstuur foto's uit een folder en stuur naar de server en verkrijg sessionID.

    Args:
       image_path: De folder waar afbeeldingen in staan

    Returns:
       De sessionID die gereturned wordt van de server
    """
    files = [("image[]", open(os.path.join(image_path, file_), "rb"))
              for file_ in os.listdir(image_path)
             if file_.endswith(".jpg") or file_.endswith(".png")]

    # Deze gare kut code moet per se van Noeel er in <-- deze comment komt uit iemand ze commit??
    index = 0
    while True:
        try:
            content = send_photos(files)
        except UploadException as e:
            # this physically hurts
            if index == 3:
                raise e

            index += 1
        else:
            break

    return content['data']['sessionId']
