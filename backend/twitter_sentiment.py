import pandas as pd
import requests
import os
import json
import tweepy
from configparser import ConfigParser
import boto3

parser = ConfigParser()
parser.read('api_auth.cfg')

#This is the super secret information that will allow access to the Twitter API and AWS Comprehend
bearer_token = parser.get('api_tracker', 'bearer_token')
aws_key_id =  parser.get('api_tracker', 'aws_key_id')
aws_key =  parser.get('api_tracker', 'aws_key')


def search_recent_tweets_as_df(query, tweet_fields):
    
    client = tweepy.Client(bearer_token=bearer_token)
    tweets = client.search_recent_tweets(query=query, tweet_fields=tweet_fields, max_results=100)
    df=pd.DataFrame(tweets.data)
    
    return df
    
def text_sentiment(df):

    client = boto3.client('comprehend',  region_name='us-west-2')

    sentiment_list = []
    sentiment_score_positive_list = []
    sentiment_score_negative_list = []
    sentiment_score_neutral_list = []
    sentiment_score_mixed_list = []

    for text in df.text:
        #text_data = base64.b64decode(text).decode('utf-8').strip()
        sentiment_all = client.detect_sentiment(Text=text, LanguageCode='en')
        sentiment_list.append(sentiment_all['Sentiment'])
        sentiment_score_positive_list.append(sentiment_all['SentimentScore']['Positive'])
        sentiment_score_negative_list.append(sentiment_all['SentimentScore']['Negative'])
        sentiment_score_neutral_list.append(sentiment_all['SentimentScore']['Neutral'])
        sentiment_score_mixed_list.append(sentiment_all['SentimentScore']['Mixed'])

    df['sentiment'] = sentiment_list
    df['sentiment_score_positive'] = sentiment_score_positive_list
    df['sentiment_score_negative'] = sentiment_score_negative_list
    df['sentiment_score_mixed'] = sentiment_score_mixed_list

    return df