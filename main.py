import logging
import os

from dotenv import load_dotenv, find_dotenv
import json
import tweepy

load_dotenv(find_dotenv())

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
access_token_key = os.environ['ACCESS_TOKEN_KEY']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)
logger = logging.getLogger("twitter")


class TwitterListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        data = json.loads(raw_data)
        if not data['favorited']:
            try:
                api.create_favorite(data['id'])
                logger.info(f"Liked the tweet of id: {data['id']}")
            except tweepy.error.TweepError:
                # @todo add more details to failure log.
                logger.error(f"Failed to like the tweet of id: {data['id']}")


streamer = tweepy.Stream(auth=api.auth, listener=TwitterListener())
streamer.filter(track=['#100daysofcode'])