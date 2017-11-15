import requests
import json
import os

class UploadException(Exception):
    pass

def _upload_photos(photos):
    headers = {"auth": "SUPER_GEHEIME_KEY"}

    r = requests.post("https://fys.1hz.nl/api/session/upload",
                      files=photos,
                      headers=headers)
    content = json.loads(r.content.decode('utf8'))

    if content['result'] == "error":
        raise UploadException(content['reason'])

    return content


def create_session(image_path):
    files = [("image[]", open(os.path.join(image_path, file_), "rb"))
              for file_ in os.listdir(image_path)
             if file_.endswith(".jpg") or file_.endswith(".png")]


    # Deze gare kut code moet per se van Noeel er in
    index = 0
    while True:
        try:
            content = _upload_photos(files)
        except UploadException as e:
            print(e.args[0])

            # this physically hurts
            if index == 3:
                raise e

            index += 1
        else:
            break

    return content['data']['sessionId']
