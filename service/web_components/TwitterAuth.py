from . import *
from flask import request
import json
import tweepy

class TwitterAuth(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/twitterAuth', TwitterAuth, ['POST'])
        self.env = env

        # when frontend request this api, this function will be called
    def view(self):
        data = request.get_json()
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

        return {'status': 'ok', 'auth': auth_dict}
    
class TwitterSignInCheck(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/twitterSignInCheck', TwitterSignInCheck, ['GET'])
        self.env = env

    def view(self):
        with open('twitter_auth.json') as json_file:
            auth_dict = json.load(json_file)
            access_token = auth_dict['access_token']
            access_token_secret = auth_dict['access_token_secret']
            consumer_key = auth_dict['consumer_key']
            consumer_secret = auth_dict['consumer_secret']

        
        # Set up OAuth and integrate with API
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Create API object
        api = tweepy.API(auth)  

        # Verify credentials
        try:
            user = api.verify_credentials()
            print("Authentication OK")
            status = 'signedIn'
            name = user.name
        except Exception as e:
            print("Error during authentication")
            print(e)
            status = 'notSignedIn'
            name = 'notSignedIn'
        #check if the access token and secret are valid
        return {'status': status, 'name': name}

class TwitterSignOut(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/twitterSignOut', TwitterSignOut, ['GET'])
        self.env = env

    def view(self):
        auth_dict = {
            'access_token': '',
            'access_token_secret': '',
            'consumer_key': "EzoH0w73hC3naY84U6NBHZHyz",
            'consumer_secret': "qjFQ5WPxqJD7C0JZtMiORkzbhYAXjNNfX0WyMdx5GWz1IiZxFw"
        }

        json_object = json.dumps(auth_dict, indent=4)

        with open('twitter_auth.json', 'w') as outfile:
            outfile.write(json_object)

        return {'status': 'signed out'}