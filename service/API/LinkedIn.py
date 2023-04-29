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

