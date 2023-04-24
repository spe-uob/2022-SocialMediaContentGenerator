from flask import Flask, request, jsonify
import json
import facebook
class FacebookBackEnd(Component):
    def __init__(self, env:Environment):
        super.__init__(env, 'api/v1/facebook', FacebookBackEnd, ['POST'])
        self.env = env

    def view(self):
        data = request.get_json()
        message = data['message']
        image_url = data['image_url']
        with open('facebook_auth.json') as json_file:
            auth_dict = json.load(json_file)
            userAccessToken = auth_dict['userAccessToken']
            pageAccessToken = auth_dict['pageAccessToken']
            pageID = auth_dict['pageID']
        graph = facebook.GraphAPI(userAccessToken)
        graph.put_object(pageID, "feed", message=message, attachment={'media': [{'type': 'image', 'src': image_url, 'href': image_url}]})


