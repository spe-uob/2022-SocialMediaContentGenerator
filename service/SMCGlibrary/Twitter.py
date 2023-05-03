from web_components import *
from flask import request
import tweepy
import io
import json


class Twitter:
    def __init__(self, env):
        self.storage = None
        self.twitter_auth = env.config['twitter_auth']
        self.load_auth()

    def load_auth(self):
        with open('twitter_auth.json') as f:
            storage = json.load(f)
        self.storage = storage

    def find_account(self, name):
        return self.storage[name]

    def post(self, name, text, images):
        tweet_string = text

        auth = tweepy.OAuthHandler(self.twitter_auth['consumer_key'], self.twitter_auth['consumer_secret'])
        auth.set_access_token(self.storage[name]['access_token'], self.storage[name]['access_token_secret'])

        api = tweepy.API(auth)
        if len(images) > 0:
            media_ids = []
            for image in images:
                res = api.media_upload(image)
                media_ids.append(res.media_id)
            api.update_status(status=text, media_ids=media_ids)
        else:
            api.update_status(tweet_string)
        return {'status': 'ok', 'tweet': tweet_string}

    def check(self, name):
        auth = tweepy.OAuthHandler(self.twitter_auth['consumer_key'], self.twitter_auth['consumer_secret'])
        auth.set_access_token(self.storage[name]['access_token'], self.storage[name]['access_token_secret'])
        api = tweepy.API(auth)
        try:
            user = api.verify_credentials()
            status = 'signedIn'
            name = user.name
        except Exception as e:
            print("Error during authentication")
            print(e)
            status = 'notSignedIn'
            name = 'notSignedIn'
        return {'status': status, 'name': name}
