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

    def post(self, name, message, images):
        pageAccessToken = self.storage[name]['pageAccessToken']
        pageID = self.storage[name]['pageId']
        photo_ids = []
        for image_path in images:
            with open(image_path, 'rb') as f:
                response = requests.post(
                    'https://graph.facebook.com/v16.0/me/photos',
                    files={'source': f},
                    data={
                        'access_token': pageAccessToken,
                        'published': 'false'
                    }
                )
            photo_ids.append(response.json()['id'])

        media_params = {
            f'attached_media[{i}]': f'{{"media_fbid":"{photo_id}"}}'
            for i, photo_id in enumerate(photo_ids)
        }
        params = {
            'access_token': pageAccessToken,
            'message': message,
            **media_params
        }
        response = requests.post(
            f'https://graph.facebook.com/v16.0/{pageID}/feed',
            params=params
        )
        return {'status': 'ok'}

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
