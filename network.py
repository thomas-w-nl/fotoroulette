import requests
import json
import os

def create_session(image_path):
    auth_key = 'SUPER_GEHEIME_KEY'
    url = 'http://fys.localhost'
    files = []

    for filename in os.listdir(image_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            fullpath = os.path.join(image_path, filename)
            files.append(('image[]', open(fullpath, 'rb')))

    headers = { 'auth': auth_key }
    r = requests.post(url + '/api/session/upload', files=files, headers=headers)
    content = json.loads(r.content.decode('latin1'))

    if content['result'] == 'success':
        return content['data']['sessionId']
    elif content['result'] == 'error':
        return content.reason
