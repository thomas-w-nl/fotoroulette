import requests
import json
import os

class NetworkingService:
    url = 'http://fys.localhost'
    auth_key = 'SUPER_GEHEIME_KEY'

    def create_session(self, image_path):

        files = []

        for filename in os.listdir(image_path):
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                fullpath = os.path.join(image_path, filename)
                files.append(('image[]', open(fullpath, 'rb')))

        headers = {'auth': self.auth_key, 'Content-Type': 'application/x-www-form-urlencoded'}
        r = requests.post(self.url + '/api/session/upload', files=files)
        print(r.content)
        exit()

        content = json.loads(r.content)

        if content.result == 'success':
            return content.data.sessionId
        elif content.result == 'error':
            return content.reason

network = NetworkingService()
network.create_session('/home/micheljonk/Pictures/fys/')
