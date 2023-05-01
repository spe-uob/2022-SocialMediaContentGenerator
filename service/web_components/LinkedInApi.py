import os.path

from . import *
from flask import request
from linkedin import linkedin
from linkedin.linkedin import PERMISSIONS
import requests
import json


class LinkedInApi(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/linkedin/access_token', 'LinkedInApi', ['GET', 'POST'])
        self.env = env

    # when frontend request this api, this function will be called
    def view(self):
        data = request.get_json()
        code = data['code']
        print(code)
        APPLICATION_KEY = '78sme225fsy5by'
        APPLICATION_SECRET = 'J3xg14qRTV87viVq'

        RETURN_URL = 'http://localhost:9000'

        authentication = linkedin.LinkedInAuthentication(
            APPLICATION_KEY,
            APPLICATION_SECRET,
            RETURN_URL,
            linkedin.PERMISSIONS.enums.values()
        )

        authentication.authorization_code = code
        result = authentication.get_access_token()

        print("Access Token:", result.access_token)
        print("Expires in (seconds):", result.expires_in)

        print(result.access_token)
        # you can get the request args by request.args.get('argName')
        arg1 = request.args.get('arg1')
        # you can reutrn a dict, it will be converted to json automatically

        application = linkedin.LinkedInApplication(token=result.access_token)
        #response = application.make_request('GET', 'https://api.linkedin.com/v2/userinfo')
        # headers = {'Authorization': 'Bearer ' + result.access_token}
        # response = requests.post('https://api.linkedin.com/v2/userinfo', headers)
        # print(response.text)
        # profile = response.text
        # profile_d = json.loads(profile)
        # user_name = profile_d['name']

        responseId = application.make_request('GET', 'https://api.linkedin.com/v2/me')

        profile = responseId.text
        profile_d = json.loads(profile)
        first_name = profile_d['firstName']['localized']['en_US']
        second_name = profile_d['lastName']['localized']['en_US']
        user_id = profile_d['id']

        user_name = first_name + " " + second_name
        if not os.path.exists("linkedin_auth.json"):
            open("linkedin_auth.json", "w").write("{}")
        with open("linkedin_auth.json", 'r') as f:
            storage = json.load(f)
        storage[user_name] = {
            "access_token": result.access_token,
            "userId": user_id
        }
        json_object = json.dumps(storage, indent=4)
        with open("linkedin_auth.json", 'w') as outfile:
            outfile.write(json_object)

        return {'status': 'ok', 'arg1': arg1}
