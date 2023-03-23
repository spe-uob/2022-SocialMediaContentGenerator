from . import *
from flask import request
import tweepy
import io


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
        access_token = data['access_token']
        access_token_secret = data['access_token_secret']
        image_base64 = data['image']
        image_path = data['image_path']

        file = io.BytesIO(base64.b64decode(image_base64))

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)
        # api.update_status(tweet_string)
        if image_path is not None and image_path != '':
            api.update_status_with_media(tweet_string, image_path)
        else:
            api.update_status_with_media(tweet_string, '1.png', file=file)
        return {'status': 'ok', 'tweet': tweet_string}
