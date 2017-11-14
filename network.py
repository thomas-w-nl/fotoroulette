import requests
import json

images_path = "/home/micheljonk/"

class NetworkingService:
    url = 'http://fys.localhost'
    auth_key = 'SUPER_GEHEIME_KEY'

    def create_session(self, data):
        headers = {'auth' : self.auth_key, 'Content-Type' : 'application/x-www-form-urlencoded'}
        r = requests.post(self.url + '/api/session/upload', data=data, headers=headers)

        content = json.loads(r.content)

        if content.result == 'success':
            return content.data.sessionId
        elif content.result == 'error':
            return content.reason

network = NetworkingService()

