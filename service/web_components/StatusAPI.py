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
        super().__init__(env, '/api/v1/Status', StatusAPI, ['POST'])
        self.env = env

    def view(self):
        data = request.get_json()
        if data['platform'] == "twitter":
            self.twitterStatusCheck(data)
        elif data['platform'] == "facebook":
            self.facebookStatusCheck(data)
        elif data['platform'] == "linkedin":
            self.linkedinStatusCheck(data)

    def twitterStatusCheck(self):
        return Twitter().check()

    def facebookStatusCheck(self):
        return Facebook().check()

    def linkedinStatusCheck(self):
        return LinkedIn().check()
