from flask import Flask, request, jsonify
import json

class FacebookBackEnd(Component):
    def __init__(self, env:Environment):
        super.__init__(env, 'api/v1/facebook', FacebookBackEnd, ['POST'])
        self.env = env

    def view(self):
        data = request.get_json()

        with open('facebook_auth.json') as json_file:
            auth_dict = json.load(json_file)
            userAccessToken = auth_dict['userAccessToken']
            pageAccessToken = auth_dict['pageAccessToken']
            pageID = auth_dict['pageID']

