# https://www.youtube.com/watch?v=8r5en18DOZQ
# https://docs.tweepy.org/en/stable/streaming.html
# SreamingClient methods
# filter() vs sample()

import re
import tweepy
import time
import boto3
from configparser import RawConfigParser

parser = RawConfigParser()
parser.read("backend/api_auth.cfg")

# This is the super secret information that will allow access to the Twitter API and AWS Comprehend
bearer_token = parser.get("api_tracker", "bearer_token")
#bearer_token = re.sub(r'"', '', bearer_token)

aws_key_id = parser.get("api_tracker", "aws_key_id")
aws_key = parser.get("api_tracker", "aws_key")

search_term = ["trading"]

def get_sentiment_based_on_text(text):
    client = boto3.client("comprehend", region_name="us-west-2")
    
    return client.detect_sentiment(Text=text, LanguageCode="en")

class MyStream(tweepy.StreamingClient):
    def on_connect(self):
        print("Connected")
    
    def on_tweet(self, tweet):
        if tweet.referenced_tweets == None:
            print(tweet.text)
            sentiment = get_sentiment_based_on_text(tweet.text)
            """
            example sentiment: {'Sentiment': 'NEUTRAL', 
                                'SentimentScore': {'Positive': 0.003268616972491145, 
                                                   'Negative': 0.3355329930782318, 
                                                   'Neutral': 0.6611716747283936, 
                                                   'Mixed': 2.6676372726797126e-05}
            """
            if sentiment['SentimentScore'][sentiment['Sentiment'].title()] >= 0.1 and sentiment['Sentiment'] != 'NEUTRAL':
                print("tweets")
                print(tweet.text)
                print("sentiment")
                print(sentiment)
            time.sleep(5)

stream = MyStream(bearer_token=bearer_token)

previousRules = stream.get_rules().data

if previousRules:
    stream.delete_rules(previousRules)

for term in search_term:
    stream.add_rules(tweepy.StreamRule(term))

stream.filter(tweet_fields=["referenced_tweets"])