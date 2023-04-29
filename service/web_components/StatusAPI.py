from . import *
from flask import Flask, request, jsonify
from linkedin import linkedin
from linkedin.linkedin import PERMISSIONS
import json
import tweepy
from service.SMCGlibrary.Twitter import Twitter
from service.SMCGlibrary.Facebook import Facebook
from service.SMCGlibrary.LinkedIn import LinkedIn

class StatusAPI(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/Post', StatusAPI, ['POST'])
        self.env = env
    
