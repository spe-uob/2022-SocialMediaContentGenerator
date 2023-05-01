from . import *
from flask import request
from linkedin import linkedin
from linkedin.linkedin import PERMISSIONS
import json
from loguru import logger


class LinkedIn:
    def __init__(self):
        with open("linkedin_auth.json") as json_file:
            self.storage = json.load(json_file)

    #         with open("linkedin_auth.json") as json_file:
    #             auth_dict = json.load(json_file)
    #             access_token = auth_dict["access_token"]
    #             APPLICATION_KEY = auth_dict["APPLICATION_KEY"]
    #             APPLICATION_SECRET = auth_dict["APPLICATION_SECRET"]
    #             profile = auth_dict["profile"]
    #         access_token = access_token
    #         self.APPLICATION_KEY = APPLICATION_KEY
    #         self.APPLICATION_SECRET = APPLICATION_SECRET
    #         self.profile = profile

    def post(self, name, text, images):
        access_token = self.storage[name]['access_token']
        user_id = self.storage[name]['userId']
        if len(images) == 0:

            url = 'https://api.linkedin.com/v2/ugcPosts'

            # Define the message to be posted
            message = {
                "author": f"urn:li:person:{user_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": f"{text}"
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

            arg1 = request.args.get('arg1')

            return {'status': 'ok', 'arg1': arg1}
        else:

            url = 'https://api.linkedin.com/rest/images?action=initializeUpload'

            message = {
                "initializeUploadRequest": {
                    "owner": f"urn:li:person:{user_id}"
                }

            }

            payload = json.dumps(message)

            response = requests.post(url,
                                     headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json', 'LinkedIn-Version': '202304', 'X-Restli-Protocol-Version': '2.0.0'},
                                     data=payload)

            logger.info(response.json())

            res = response.json()
            uploadUrl = res['value']['uploadUrl']
            image_id = res['value']['image']

            responseImage = requests.put(uploadUrl, headers={'X-Restli-Protocol-Version': '2.0.0', 'Authorization': 'Bearer ' + access_token, 'LinkedIn-Version': '202304'},
                                         data=open(images[0], "rb"))

            responseImage.raise_for_status()


            message = "testing api"

            post_d = {
                "author": f"urn:li:person:{user_id}",
                "commentary": text,
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
            r = requests.post("https://api.linkedin.com/rest/posts",
                              headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json', 'X-Restli-Protocol-Version': '2.0.0', 'LinkedIn-Version': '202304'}, data=payload)

            logger.info(r.text)

            # you can reutrn a dict, it will be converted to json automatically
            return {'status': 'ok', 'url': uploadUrl}

    def check(self):
        try:
            status = "signedIn"
            name = self.profile['firstName'] + " " + self.profile['lastName']
        except linkedin.LinkedInError as e:
            status = "notSignedIn"
            name = ""
        return {'status': status, 'name': name}
