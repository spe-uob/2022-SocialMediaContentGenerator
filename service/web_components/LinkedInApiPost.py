from . import *
from flask import request
import requests
from linkedin import linkedin
from linkedin.linkedin import PERMISSIONS
from linkedin import server
import json


class LinkedInApiPost(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/linkedin/post', 'linkedInApiPost', ['GET', 'POST'])
        self.env = env

    # when frontend request this api, this function will be called
    def view(self):

        data = request.get_json()
        message = data['message']
        print(message)

        with open("linkedin_auth.json") as json_file:
                    auth_dict = json.load(json_file)
                    access_token = auth_dict["access_token"]
        """ application = server.quick_api('78sme225fsy5by', 'J3xg14qRTV87viVq') """
        print(access_token)
        print("hello")

        application = linkedin.LinkedInApplication(token= access_token)
        print("HHEEERRRREEEE")
        response = application.make_request('GET', 'https://api.linkedin.com/v2/me')
        print(response.text)
        profile = response.text
        profile_d = json.loads(profile)
        user_id = profile_d['id']
        print(user_id)


        url = 'https://api.linkedin.com/v2/ugcPosts'

        # Define the message to be posted
        message = {
            "author": f"urn:li:person:{user_id}",
                  "lifecycleState": "PUBLISHED",
                  "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                      "shareCommentary": {
                        "text": f"{message}"
                      },
                      "shareMediaCategory": "NONE"
                    }
                  },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        # Convert the message to JSON format
        payload = json.dumps(message)

        # Make the API request to post the message
        response = requests.post(url, headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json', 'X-Restli-Protocol-Version': '2.0.0'}, data=payload)

        # Print the API response
        print(response.json())


        # you can get the request args by request.args.get('argName')"""
        arg1 = request.args.get('arg1')
        # you can reutrn a dict, it will be converted to json automatically
        return {'status': 'ok', 'arg1': arg1}
