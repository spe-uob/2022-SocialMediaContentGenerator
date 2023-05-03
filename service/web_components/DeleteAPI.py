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


class DeleteAPI(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/Delete', 'DeleteAPI', ['POST'])
        self.env = env

    def view(self):
        data = request.get_json()
        if data['platform'] == "twitter":
            self.delete_twitter_account(data)
        elif data['platform'] == "facebook":
            self.delete_facebook_account(data)
        elif data['platform'] == "linkedin":
            self.delete_linkedin_account(data)
        return {"status": 0}

    def delete_twitter_account(self, data):
        with open('twitter_auth.json', 'r') as f:
            storage = json.load(f)
        del storage[data['name']]
        with open('twitter_auth.json', 'w') as f:
            json.dump(storage, f)

    def delete_facebook_account(self, data):
        with open('facebook_auth.json', 'w') as f:
            storage = json.load(f)
        del storage[data['name']]
        with open('facebook_auth.json', 'w') as f:
            json.dump(storage, f)

    def delete_linkedin_account(self, data):
        with open('linkedin_auth.json', 'w') as f:
            storage = json.load(f)
        del storage[data['name']]
        with open('linkedin_auth.json', 'w') as f:
            json.dump(storage, f)
