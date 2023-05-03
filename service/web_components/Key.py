from . import *


class Key(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/key', Key, ['GET'])
        self.env = env
        self.twitter_auth = self.env.config["twitter_auth"]
        self.linkedin_auth = self.env.config["linkedin_auth"].copy()
        self.facebook_auth = self.env.config["facebook_auth"]
        self.linkedin_auth["application_secret"] = ""

    def view(self):
        return {"twitter_auth": self.twitter_auth, "linkedin_auth": self.linkedin_auth, "facebook_auth": self.facebook_auth}
