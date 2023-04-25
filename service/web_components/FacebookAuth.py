from flask import Flask, request, jsonify
import json


class FacebookAuth(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/twitterAuth', FacebookAuth, ['POST'])
        self.env = env

    def view(self):
        data = request.get_json()
        userAccessToken = data['userAccessToken']
        pageAccessToken = data['pageAccessToken']
        pageID = data['pageID']
        auth_dict = {
            'userAccessToken': userAccessToken,
            'pageAccessToken': pageAccessToken,
            'pageId': pageID
        }

        json_object = json.dumps(auth_dict, indent=3)

        with open('facebook_auth.json', 'w') as outfile:
            outfile.write(json_object)

        return {'status': 'ok', 'auth': auth_dict}
