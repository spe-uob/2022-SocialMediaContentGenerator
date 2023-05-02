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

class LinkedInApiPostImage(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/LinkedInApiPostImage', 'LinkedInApiPostImage', ['GET', 'POST'])
        self.env = env

    # when frontend request this api, this function will be called
    def view(self):

        textMessage = request.files['message']
        image = request.files['image']
        #image = data.read()





        with open("linkedin_auth.json") as json_file:
                            auth_dict = json.load(json_file)
                            access_token = auth_dict["access_token"]

        application = linkedin.LinkedInApplication(token= access_token)
        print("HHEEERRRREEEE 2222")
        response = application.make_request('GET', 'https://api.linkedin.com/v2/me')
        print(response.text)
        profile = response.text
        profile_d = json.loads(profile)
        user_id = profile_d['id']

        url = 'https://api.linkedin.com/rest/images?action=initializeUpload'

        message = {
                       "initializeUploadRequest": {
                              "owner": f"urn:li:person:{user_id}"
                        }

                  }

        payload = json.dumps(message)

        response = requests.post(url, headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json', 'LinkedIn-Version': '202304' , 'X-Restli-Protocol-Version': '2.0.0'}, data=payload)

        print(response.json())

        res = response.json()
        uploadUrl = res['value']['uploadUrl']
        image_id = res['value']['image']



        responseImage = requests.put(uploadUrl, headers={'X-Restli-Protocol-Version': '2.0.0', 'Authorization': 'Bearer ' + access_token, 'LinkedIn-Version': '202304'}, data = image)

        responseImage.raise_for_status()

        message = "testing api"






        post_d = {
                   "author": f"urn:li:person:{user_id}",
                   "commentary": textMessage,
                   "visibility": "PUBLIC",
                   "distribution": {
                     "feedDistribution": "MAIN_FEED",
                     "targetEntities": [],
                     "thirdPartyDistributionChannels": []
                   },
                   "content": {
                     "media": {
                       "title":"title of the video",
                       "id": image_id
                     }
                   },
                   "lifecycleState": "PUBLISHED",


                 }

        payload = json.dumps(post_d)
        r = requests.post("https://api.linkedin.com/rest/posts", headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json', 'X-Restli-Protocol-Version': '2.0.0', 'LinkedIn-Version': '202304'}, data=payload)


        print("here")
        """ print(r.json()) """



        # you can reutrn a dict, it will be converted to json automatically
        return {'status': 'ok', 'url': uploadUrl}

class LinkedInApiGetPosts(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/LinkedInApiGetPosts', 'LinkedInApiGetPosts', ['GET', 'POST'])
        self.env = env

    def view(self):

        with open("linkedin_auth.json") as json_file:
                auth_dict = json.load(json_file)
                access_token = auth_dict["access_token"]

                application = linkedin.LinkedInApplication(token= access_token)
                print("HHEEERRRREEEE 2222")
                response = application.make_request('GET', 'https://api.linkedin.com/v2/me')
                print(response.text)
                profile = response.text
                profile_d = json.loads(profile)
                user_id = profile_d['id']

        headers = {
                "Authorization": f"Bearer {access_token}",
                "cache-control": "no-cache",
                "X-Restli-Protocol-Version": "2.0.0"
            }

            # define the request parameters
        params = {
                "q": "authors",
                "authors": f"urn:li:person:{user_id}",
                "projection": "(id,created,specificContent(text))"
            }
        linkedin_api_endpoint = "https://api.linkedin.com/v2/shares"
        # make the GET request to the LinkedIn API
        response = requests.get(linkedin_api_endpoint, headers=headers, params=params)

        # parse the response and return the posts
        posts = []
        if response.ok:
            data = response.json()
            for share in data.get("elements", []):
                post = {
                    "id": share.get("id"),
                    "text": share.get("specificContent", {}).get("text", {}).get("text")
                }
                posts.append(post)

        print(len(posts))
        return {'status': 'ok', 'posts': posts}


