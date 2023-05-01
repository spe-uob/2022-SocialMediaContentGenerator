import os

from . import *
from flask import Flask, request, jsonify
from linkedin import linkedin
from linkedin.linkedin import PERMISSIONS
import json
import tweepy
import facebook
from SMCGlibrary.Twitter import Twitter
from SMCGlibrary.Facebook import Facebook
from SMCGlibrary.LinkedIn import LinkedIn


class StatusAPI(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/account_status', StatusAPI, ['GET', 'POST'])
        self.env = env

    def view(self):
        twitter_storage = self.load_cache('twitter_auth.json')
        facebook_storage = self.load_cache('facebook_auth.json')
        linkedin_storage = self.load_cache('linkedin_auth.json')
        result = []
        for name in twitter_storage:
            result.append({'platform': 'twitter', 'name': name, 'status': self.twitterStatusCheck()})
        for name in facebook_storage:
            result.append({'platform': 'facebook', 'name': name, 'status': self.facebookStatusCheck()})
        for name in linkedin_storage:
            result.append({'platform': 'linkedin', 'name': name, 'status': self.linkedinStatusCheck()})
        return result

    @staticmethod
    def load_cache(filename):
        if not os.path.exists(filename):
            return {}
        with open(filename, 'r') as f:
            storage = json.load(f)
        return storage

    def twitterStatusCheck(self):
        return {}  # Twitter().check()

    def facebookStatusCheck(self):
        return {}  # Facebook().check()

    def linkedinStatusCheck(self):
        return {}  # LinkedIn().check()
