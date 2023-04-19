from . import *
from flask import request
from linkedin import linkedin
from linkedin.linkedin import PERMISSIONS

class LinkedInApi(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/linkedin/access_token', 'LinkedInApi', ['GET', 'POST'])
        self.env = env

    # when frontend request this api, this function will be called
    def view(self):
        data = request.get_json()
        code = data['code']
        authentication.authorization_code = code
        access_token = authentication.get_access_token()
        # you can get the request args by request.args.get('argName')
        arg1 = request.args.get('arg1')
        # you can reutrn a dict, it will be converted to json automatically
        return {'status': 'ok', 'arg1': arg1}