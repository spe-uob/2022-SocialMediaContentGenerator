from flask import Flask, request, jsonify
class TwitterAuth(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/twitterAuth', TwitterAuth, ['POST'])
        self.env = env

    def view(self):
        data = request.get_json()
        userAccessToken = data['userAccessToken']
        access_token_secret = data['access_token_secret']

        auth_dict = {
        'access_token': access_token,
        'access_token_secret': access_token_secret,
        'consumer_key': "EzoH0w73hC3naY84U6NBHZHyz",
        'consumer_secret': "qjFQ5WPxqJD7C0JZtMiORkzbhYAXjNNfX0WyMdx5GWz1IiZxFw"
        }

        json_object = json.dumps(auth_dict, indent=4)

        with open('twitter_auth.json', 'w') as outfile:
         outfile.write(json_object)

        return {'status': 'ok', 'auth': auth_dict}