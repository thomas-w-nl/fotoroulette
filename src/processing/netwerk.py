import requests
import json
import os
import numpy as np

"""
Created Exception so we can catch it
"""
class UploadException(Exception):
    pass

"""
Send photos to server and get SessionId
"""
def send_photos(photos) -> np.array:
    headers = {"auth": "SUPER_GEHEIME_KEY"}

    r = requests.post("https://fys.1hz.nl/api/session/upload",
                      files=photos,
                      headers=headers)
    content = json.loads(r.content.decode('utf8'))

    if content['result'] == "error":
        raise UploadException(content['reason'])

    return content

"""
Get images from directory and send to server
"""
def send_photos_by_path(image_path):
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