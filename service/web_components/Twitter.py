from . import *
from flask import request
import tweepy
import io
import json

class TwitterBackEnd(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1//twitter', TwitterBackEnd, ['GET', 'POST'])
        self.env = env

        # when frontend request this api, this function will be called
    def view(self):
        data = request.get_json()
        tweet_string = data['status']
        consumer_key = data['consumer_key']
        consumer_secret = data['consumer_secret']
        image_base64 = data['image']

        file = io.BytesIO(base64.b64decode(image_base64))

        with open('twitter_auth.json') as json_file:
            auth_dict = json.load(json_file)
            access_token = auth_dict['access_token']
            access_token_secret = auth_dict['access_token_secret']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)
        if image_base64:
            api.update_status_with_media(tweet_string, '1.png', file=file)
        else:
            api.update_status(tweet_string)
        return {'status': 'ok', 'tweet': tweet_string}