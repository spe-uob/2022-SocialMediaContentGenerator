from flask import Flask, request, jsonify
import json
import facebook


class Facebook:
    def __init__(self):
        with open('facebook_auth.json') as json_file:
            auth_dict = json.load(json_file)
            userAccessToken = auth_dict['userAccessToken']
            pageAccessToken = auth_dict['pageAccessToken']
            pageID = auth_dict['pageID']
        self.userAccessToken = userAccessToken
        self.pageAccessToken = pageAccessToken
        self.pageID = pageID

    def post(self, message, image):
        graph = facebook.GraphAPI(self.userAccessToken)
        graph.put_object(self.pageID, "feed", message=message,
                         attachment={'media': [{'type': 'image', 'src': image, 'href': image}]})

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
