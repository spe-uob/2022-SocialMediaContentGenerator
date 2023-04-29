from . import *
from flask import Flask, request, jsonify
from linkedin import linkedin
from linkedin.linkedin import PERMISSIONS
import json
import tweepy
from service.SMCGlibrary.Twitter import Twitter
from service.SMCGlibrary.Facebook import Facebook
from service.SMCGlibrary.LinkedIn import LinkedIn

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
        
    def facebookPost(self, data):

    def linkedinPost(self, data):

