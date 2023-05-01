import requests
from flask import Flask, request, jsonify
import json
import facebook


class Facebook:
    def __init__(self):
        self.storage = None
        self.load_auth()

    def load_auth(self):
        with open('facebook_auth.json') as f:
            storage = json.load(f)
        self.storage = storage

    def _post(self, name, message, images):
        graph = facebook.GraphAPI(self.storage[name]['pageAccessToken'])
        graph.put_object(self.storage[name]["pageId"], "feed", message=message,
                         attached=[open(image, "rb").read() for image in images])

    def post(self, name, message, images):
        post_data = {
            'access_token': self.storage[name]['pageAccessToken'],
            'published': 'true'
        }
        for i, image in enumerate(images):
            image_file = open(image, 'rb')
            image_data = {
                'filename': f'image{i}.jpg',
                'content_type': 'image/jpeg',
                'file': image_file
            }
            response = requests.post(
                f'https://graph.facebook.com/{self.storage[name]["pageId"]}/photos',
                data=post_data,
                files={'source': image_data}
            )
            print(response.json())
        pass

    def check(self):
        graph = facebook.GraphAPI(access_token=self.userAccessToken, version='16.0')
        try:
            profile = graph.get_object(id='me')
            status = "signedIn"
            name = profile['name']
        except facebook.GraphAPIError as e:
            status = "notSignedIn"
            name = ""
        return {'status': status, 'name': name}
