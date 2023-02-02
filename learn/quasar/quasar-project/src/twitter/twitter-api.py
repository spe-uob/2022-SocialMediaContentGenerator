import tweepy
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

class Tweet(Resource):
  def get(self):
      tweet_string = request.args.get('status')
      consumer_key = request.args.get('consumer_key')
      consumer_secret = request.args.get('consumer_secret')
      access_token = request.args.get('access_token')
      access_token_secret = request.args.get('access_token_secret')

      auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_token, access_token_secret)

      api = tweepy.API(auth)
      api.update_status(tweet_string)

      return jsonify({'status': 'success'})

api.add_resource(Tweet, '/tweet')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
