from . import *
from flask import request
import json

class TwitterAuth(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/twitterAuth', TwitterAuth, ['POST'])
        self.env = env

        # when frontend request this api, this function will be called
    def view(self):
        data = request.get_json()
        access_token = data['access_token']
        access_token_secret = data['access_token_secret']

        auth_dict = {
            'access_token': access_token,
            'access_token_secret': access_token_secret
        }

        json_object = json.dumps(auth_dict, indent=4)

        with open('twitter_auth.json', 'w') as outfile:
            outfile.write(json_object)

        return {'status': 'ok', 'auth': auth_dict}