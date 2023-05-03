import os

import facebook

from . import *
from flask import Flask, request, jsonify
from linkedin import linkedin
from linkedin.linkedin import PERMISSIONS
import json
import tweepy
from SMCGlibrary.Twitter import Twitter
from SMCGlibrary.Facebook import Facebook
from SMCGlibrary.LinkedIn import LinkedIn

class TimelineAPI(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/Timeline', TimelineAPI, ['POST'])
        self.env = env

    def view(self):
        data = request.get_json()
        if data['platform'] == "twitter":
            response = self.Twitter_Timeline_Name(self,data)
        return {"status": 0}

    def Twitter_Timeline_Name(self,data):
        with open('twitter_auth.json', 'r') as f:
            storage = json.load(f)
            res = {"name": storage[0]}

