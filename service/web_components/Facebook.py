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
        image = data['image']
        with open('facebook_auth.json') as json_file:
            auth_dict = json.load(json_file)
            userAccessToken = auth_dict['userAccessToken']
            pageAccessToken = auth_dict['pageAccessToken']
            pageID = auth_dict['pageID']
        graph = facebook.GraphAPI(access_token = userAccessToken, version='16.0')
        photo_id = graph.put_photo(image=image)
        graph.put_object(parent_object=pageID, connection_name='feed', message=message,
                         picture='https://www.facebook.com/photo.php?fbid=' + photo_id)


