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
        self.access_token = access_token

    def post(self, text):
        image = request.files['image']
        url = 'https://api.linkedin.com/rest/images?action=initializeUpload'
        application = linkedin.LinkedInApplication(token=self.access_token)
        response = application.make_request('GET', 'https://api.linkedin.com/v2/me')
        profile = response.text
        profile_d = json.loads(profile)
        user_id = profile_d['id']
        message = {
            "initializeUploadRequest": {
                "owner": f"urn:li:person:{user_id}"
            }
        }
        payload = json.dumps(message)
        response = request.post(url,
                                headers={'Authorization': 'Bearer ' + self.access_token,
                                         'Content-Type': 'application/json',
                                         'LinkedIn-Version': '202304', 'X-Restli-Protocol-Version': '2.0.0'},
                                data=payload)
        res = response.json()
        uploadUrl = res['value']['uploadUrl']
        image_id = res['value']['image']
        responseImage = request.put(uploadUrl, headers={'X-Restli-Protocol-Version': '2.0.0',
                                                        'Authorization': 'Bearer ' + self.access_token,
                                                        'LinkedIn-Version': '202304'}, data=image)
        responseImage.raise_for_status()
        post_d = {
            "author": f"urn:li:person:{user_id}",
            "commentary": "Sample video Post",
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "content": {
                "media": {
                    "title": "title of the video",
                    "id": image_id
                }
            },
            "lifecycleState": "PUBLISHED",
        }

        payload = json.dumps(post_d)
        r = request.post("https://api.linkedin.com/rest/posts",
                          headers={'Authorization': 'Bearer ' + self.access_token, 'Content-Type': 'application/json',
                                   'X-Restli-Protocol-Version': '2.0.0', 'LinkedIn-Version': '202304'}, data=payload)
