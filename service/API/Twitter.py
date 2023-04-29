from service.web_components import *
from flask import request
import tweepy
import io
import json

class Twitter:
    def __init__(self):
        with open('twitter_auth.json') as json_file:
            auth_dict = json.load(json_file)
            access_token = auth_dict['access_token']
            access_token_secret = auth_dict['access_token_secret']
            consumer_key = auth_dict['consumer_key']
            consumer_secret = auth_dict['consumer_secret']
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def post(self, status, image):
        tweet_string = status
        image_base64 = image

        file = io.BytesIO(base64.b64decode(image_base64))

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        api = tweepy.API(auth)
        if image_base64:
            api.update_status_with_media(tweet_string, '1.png', file=file)
        else:
            api.update_status(tweet_string)
        return {'status': 'ok', 'tweet': tweet_string}
