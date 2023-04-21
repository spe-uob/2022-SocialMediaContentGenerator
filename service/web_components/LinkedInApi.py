from . import *
from flask import request
""" from linkedin import linkedin """ 
from linkedin.linkedin import PERMISSIONS
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

        print ("Access Token:", result.access_token)
        print ("Expires in (seconds):", result.expires_in)


        print(result.access_token)
        # you can get the request args by request.args.get('argName')
        arg1 = request.args.get('arg1')
        # you can reutrn a dict, it will be converted to json automatically
        auth_dict = {
        "access_token": result.access_token
        }
        json_object = json.dumps(auth_dict, indent=4)
        with open("linkedin_auth.json", 'w') as outfile:
            outfile.write(json_object)

        return {'status': 'ok', 'arg1': arg1}

