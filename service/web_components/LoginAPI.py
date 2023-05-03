import os

import facebook

from . import *
from flask import Flask, request, jsonify
from linkedin import linkedin
from linkedin.linkedin import PERMISSIONS
import json
import tweepy
from SMCGlibrary.Twitter import Twitter
from SMCGlibrary.Facebook import Facebook
from SMCGlibrary.LinkedIn import LinkedIn


class LoginAPI(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/Login', LoginAPI, ['POST'])
        self.env = env
        self.twitter_auth = self.env.config["twitter_auth"]
        self.linkedin_auth = self.env.config["linkedin_auth"]

    def view(self):
        data = request.get_json()
        if data['platform'] == "twitter":
            self.logged_twitter_account(data)
        elif data['platform'] == "facebook":
            self.logged_facebook_account(data)
        elif data['platform'] == "linkedin":
            self.logged_linkedin_account(data)
        return {"status": 0}

    def logged_twitter_account(self, data):
        access_token = data['access_token']
        access_token_secret = data['access_token_secret']
        storage = {}
        if not os.path.exists('twitter_auth.json'):
            with open('twitter_auth.json', 'w') as f:
                json.dump(storage, f)
        with open('twitter_auth.json', 'r') as f:
            storage = json.load(f)
        status = self.get_twitter_name(self.twitter_auth['consumer_key'], self.twitter_auth['consumer_secret'], access_token, access_token_secret)
        storage[status['name']] = {
            'access_token': access_token,
            'access_token_secret': access_token_secret
        }
        json_object = json.dumps(storage, indent=4)
        with open('twitter_auth.json', 'w') as outfile:
            outfile.write(json_object)

    @staticmethod
    def get_twitter_name(consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        api = tweepy.API(auth)
        user = api.verify_credentials()
        status = 0
        name = user.screen_name
        return {'status': status, 'name': name}

    def logged_facebook_account(self, data):
        user_access_token = data['userAccessToken']
        page_access_token = data['pageAccessToken']
        page_id = data['pageId']
        storage = {}
        if not os.path.exists('facebook_auth.json'):
            with open('facebook_auth.json', 'w') as f:
                json.dump(storage, f)
        with open('facebook_auth.json', 'r') as f:
            storage = json.load(f)
        status = self.get_facebook_name(user_access_token)
        storage[status['name']] = {
            'userAccessToken': user_access_token,
            'pageAccessToken': page_access_token,
            'pageId': page_id
        }
        json_object = json.dumps(storage, indent=4)
        with open('facebook_auth.json', 'w') as outfile:
            outfile.write(json_object)

    @staticmethod
    def get_facebook_name(user_access_token):
        graph = facebook.GraphAPI(access_token=user_access_token)
        try:
            profile = graph.get_object(id='me')
            status = 0
            name = profile['name']
        except facebook.GraphAPIError as e:
            status = 1
            name = None
        return {'status': status, 'name': name}

    def logged_linkedin_account(self, data):
        code = data['code']
        url = data['url']
        application_key = self.linkedin_auth['application_key']
        application_secret = self.linkedin_auth['application_secret']
        authentication = linkedin.LinkedInAuthentication(application_key, application_secret, url, linkedin.PERMISSIONS.enums.values())
        authentication.authorization_code = code
        result = authentication.get_access_token()
        profile = authentication.get_profile(selectors=['id', 'first-name', 'last-name'])
        auth_dict = {
            "access_token": result.access_token,
            "APPLICATION_KEY": '78sme225fsy5by',
            "APPLICATION_SECRET": 'J3xg14qRTV87viVq',
            "profile": profile
        }
        json_object = json.dumps(auth_dict, indent=4)
        with open("linkedin_auth.json", 'w') as outfile:
            outfile.write(json_object)
