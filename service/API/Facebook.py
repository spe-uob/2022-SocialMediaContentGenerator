from flask import Flask, request, jsonify
import json


class Facebook:
    def __init__(self):
        with open('facebook_auth.json') as json_file:
            auth_dict = json.load(json_file)
            userAccessToken = auth_dict['userAccessToken']
            pageAccessToken = auth_dict['pageAccessToken']
            pageID = auth_dict['pageID']
        self.userAccessToken = userAccessToken
        self.pageAccessToken = pageAccessToken
        self.pageID = pageID
