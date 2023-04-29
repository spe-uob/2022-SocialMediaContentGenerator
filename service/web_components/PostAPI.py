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
    def __init__(self,env:Environment):
        super().__init__(env,'/api/v1/Post',PostAPI,['POST'])
        self.env = env
    def view(self):
        data = request.get_json()
        if data['platform'] == "twitter":
            self.twitterPost(data)
        elif data['platform'] == "facebook":
            self.facebookPost(data)
        elif data['platform'] == "linkedin":
            self.linkedinPost(data)
    def twitterPost(self, data):
        tweet_string = data['status']
        image_base64 = data['image']
        Twitter().post(Twitter,tweet_string,image_base64)
    def facebookPost(self, data):
        message = data['message']
        image_url = data['image_url']
        Facebook().post(Facebook, message, image_url)
    def linkedinPost(self, data):
        text = data['text']
        image = data['image']
        LinkedIn().post(LinkedIn, text, image)




