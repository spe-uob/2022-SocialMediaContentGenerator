from . import *
from flask import Flask, request, jsonify
from linkedin import linkedin
from linkedin.linkedin import PERMISSIONS
import json
import tweepy
from SMCGlibrary.Twitter import Twitter
from SMCGlibrary.Facebook import Facebook
from SMCGlibrary.LinkedIn import LinkedIn


class PostAPI(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/post', PostAPI, ['POST'])
        self.env = env

    def view(self):
        data = request.get_json()
        text = data['text']
        images = data['images']
        accounts = data['accounts']
        for account in accounts:
            platform = account['platform']
            name = account['name']
            if platform == "twitter":
                self.twitter_post(name, text, images)
            elif platform == "facebook":
                self.facebook_post(name, text, images)
            elif platform == "linkedin":
                self.linkedin_post(name, text, images)
        return {}

    def twitter_post(self, name, text, images):
        Twitter(self.env).post(name, text, images)

    @staticmethod
    def facebook_post(name, text, images):
        Facebook().post(name, text, images)

    @staticmethod
    def linkedin_post(name, text, images):
        LinkedIn().post(name, text, images)
