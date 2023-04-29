from . import *
from flask import Flask, request, jsonify
from linkedin import linkedin
from linkedin.linkedin import PERMISSIONS
import json
import tweepy
from service.SMCGlibrary.Twitter import Twitter
from service.SMCGlibrary.Facebook import Facebook
from service.SMCGlibrary.LinkedIn import LinkedIn


class LoginAPI(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/Login', LoginAPI, ['POST'])
        self.env = env

    def view(self):
        data = request.get_json()
        if data['platform'] == "twitter":
            self.twitterAuth(data)
        elif data['platform'] == "facebook":
            self.facebookAuth(data)
        elif data['platform'] == "linkedin":
            self.linkedinAuth(data)

    def twitterAuth(self, data):
        access_token = data['access_token']
        access_token_secret = data['access_token_secret']
        auth_dict = {
            'access_token': access_token,
            'access_token_secret': access_token_secret,
            'consumer_key': "EzoH0w73hC3naY84U6NBHZHyz",
            'consumer_secret': "qjFQ5WPxqJD7C0JZtMiORkzbhYAXjNNfX0WyMdx5GWz1IiZxFw"
        }
        json_object = json.dumps(auth_dict, indent=4)
        with open('twitter_auth.json', 'w') as outfile:
            outfile.write(json_object)

    def facebookAuth(self, data):
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


