import logging
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

import twitter_sentiment

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

app = FastAPI()


class Keyword(BaseModel):
    pagename: str


@app.post("/")
def get_pagename(keyword: Keyword):

    query = f"from:{keyword.pagename} -is:retweet" # get reply, 'conversation_id:1471510774505893906'
    tweet_fields = ["context_annotations", "created_at", "conversation_id"]

    df = twitter_sentiment.search_recent_tweets_as_df(query, tweet_fields)
    df_sentiment = twitter_sentiment.text_sentiment(df)

    df_sentiment["max_score"] = df_sentiment[
        [
            "sentiment_score_positive",
            "sentiment_score_negative",
            "sentiment_score_mixed",
        ]
    ].max(axis=1)
    df_sentiment = (
        df_sentiment[
            [
                "text",
                "created_at",
                "sentiment",
                "sentiment_score_positive",
                "sentiment_score_negative",
                "sentiment_score_mixed",
                "max_score",
            ]
        ]
        .sort_values(by=["created_at"], ascending=False)
        .reset_index(drop=True)
    )

    return df_sentiment.to_json()


if __name__ == "__main__":
    logging.info("Starting backend server")
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
