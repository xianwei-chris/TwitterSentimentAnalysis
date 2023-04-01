# https://www.youtube.com/watch?v=8r5en18DOZQ
# https://docs.tweepy.org/en/stable/streaming.html
# https://blacksheephacks.pl/stream-data-with-python-and-aws-kinesis/
# SreamingClient methods
# filter() vs sample()

import tweepy
from datetime import datetime, timezone
import boto3
import json
from configparser import RawConfigParser

from backend.ingestion import constants


class MyStream(tweepy.StreamingClient):
    
    def __init__(self, bearer_token):
        tweepy.StreamingClient.__init__(self, bearer_token)
        self.i = 0
        self.previousRules = self.get_rules().data
        if self.previousRules:
            self.delete_rules(self.previousRules)

        for term in constants.search_term:
            self.add_rules(tweepy.StreamRule(term))

        self.filter(tweet_fields=["referenced_tweets"])


    def on_connect(self):
        print("Connected")
    
    def stream_to_kinesis(self, data):
        kinesis_client = boto3.client('kinesis', region_name='us-east-1')
        kinesis_client.put_record(StreamName=constants.STREAM_NAME,
                                  Data=json.dumps(data),
                                  PartitionKey="partitionkey")

    def on_tweet(self, tweet):
        if tweet.referenced_tweets == None:
            self.i += 1
            data={'event_time': datetime.now(timezone.utc).isoformat(),
            'index': self.i,
            'tweet_text': tweet.text}
            print(data)
            self.stream_to_kinesis(data)


if __name__ == "__main__":

    parser = RawConfigParser()
    parser.read("backend/api_auth.cfg")

    bearer_token = parser.get("api_tracker", "bearer_token")
    aws_key_id = parser.get("api_tracker", "aws_key_id")
    aws_key = parser.get("api_tracker", "aws_key")

    search_term = constants.search_term

    stream = MyStream(bearer_token=bearer_token)
