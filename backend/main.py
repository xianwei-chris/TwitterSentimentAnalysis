# backend/main.py

import uuid
import uvicorn
from fastapi import File
from fastapi import FastAPI
from fastapi import UploadFile
import numpy as np
from pydantic import BaseModel

import twitter_sentiment

app = FastAPI()

class Keyword(BaseModel):
    pagename: str

@app.post("/")
def get_pagename(keyword: Keyword):

    query = f'from:{keyword.pagename} -is:retweet' #get reply, 'conversation_id:1471510774505893906'
    tweet_fields = ['context_annotations', 'created_at','conversation_id']

    df = twitter_sentiment.search_recent_tweets_as_df(query, tweet_fields)
    df_sentiment = twitter_sentiment.text_sentiment(df)
    print(df_sentiment.head())

    return {"page_name": keyword.pagename,
            "sample_text": df.text[1],
            "sentiment_score":df_sentiment.sentiment[1]
            }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
