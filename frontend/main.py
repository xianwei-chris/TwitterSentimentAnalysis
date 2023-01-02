import requests
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# defines an h1 header
st.title("Tweets Sentiment")
st.markdown(
    "This webapp allows users to input Twitter page name, and it will return recent tweets from that page and respective sentiment scores.  \
User can use it to understand the overall sentiment on a certain page or keyword. Eg pagename:'Bitoin'"
)

# displays a file uploader widget
keyword = st.text_area("Input twitter page name for sample_text")
data = {"pagename": keyword}

# displays a button
if st.button("Get Sentiment"):
    if keyword:

        res = requests.post(f"http://backend:8080/", json=data)
        res_json = res.json()

    st.text("Most recent tweets from Pagename:" + keyword + " order by descending time")
    df_sentiment = pd.read_json(res_json)
    st.dataframe(data=df_sentiment)

    fig = plt.figure(figsize=(10, 4))
    plt.title("Frequency of tweets positive score")
    sns.histplot(
        df_sentiment, x="sentiment_score_positive", bins=[0, 0.2, 0.4, 0.6, 0.8, 1]
    )
    st.pyplot(fig)

    fig = plt.figure(figsize=(10, 4))
    plt.title("Frequency of tweets negative score")
    sns.histplot(
        df_sentiment, x="sentiment_score_negative", bins=[0, 0.2, 0.4, 0.6, 0.8, 1]
    )
    st.pyplot(fig)

    fig = plt.figure(figsize=(10, 4))
    plt.title("Frequency of tweets mixed score")
    sns.histplot(
        df_sentiment, x="sentiment_score_mixed", bins=[0, 0.2, 0.4, 0.6, 0.8, 1]
    )
    st.pyplot(fig)
