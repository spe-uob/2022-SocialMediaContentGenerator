from . import *
from flask import request
import json
import tweepy

class TwitterAPI (Component):
    def __init__(self, env:Environment):
        super().__init__(env, '/api/v1/Twitter', TwitterAPI, ['POST'])
        self.env = env