from . import *
from flask import request
from linkedin import linkedin
from linkedin.linkedin import PERMISSIONS
import json


class LinkedIn:
    def __init__(self):
        with open("linkedin_auth.json") as json_file:
            auth_dict = json.load(json_file)
            access_token = auth_dict["access_token"]
            APPLICATION_KEY = auth_dict["APPLICATION_KEY"]
            APPLICATION_SECRET = auth_dict["APPLICATION_SECRET"]
            profile = auth_dict["profile"]
        self.access_token = access_token
        self.APPLICATION_KEY = APPLICATION_KEY
        self.APPLICATION_SECRET = APPLICATION_SECRET
        self.profile = profile

    def post(self, text, image):
        application = linkedin.LinkedInApplication(token=self.access_token)
        image_url = image
        image_data = application.submit_image(image_url=image_url)
        text = text
        post_data = {
            'comment': text,
            'content': {
                'submitted-url': 'https://example.com/',
                'submitted-image-url': image_data['id']
            },
            'visibility': {
                'code': 'anyone'
            }
        }
        response = application.submit_share(**post_data)

    def check(self):
        try:
            status = "signedIn"
            name = self.profile['firstName'] + " " + self.profile['lastName']
        except linkedin.LinkedInError as e:
            status = "notSignedIn"
            name = ""
        return {'status': status, 'name': name}





