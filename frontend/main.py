# frontend/main.py

import requests
import streamlit as st

# defines an h1 header
st.title("Tweets Sentiment")
st.markdown("This webapp allows users to input Twitter Page name, and it will return recent tweets from that page and respective sentiment scores.  \
User can use it to understand the overall sentiment on a certain page or keyword")

# displays a file uploader widget
keyword = st.text_area("Input twitter page name for sample_text")
data = {'pagename':keyword}

# displays a button
if st.button("Get Sentiment"):
    if keyword:

        res = requests.post(f"http://0.0.0.0:8080/", json=data)
        #res = requests.post(f"http://backend:8080/", json=data)
        sentiment = res.json()
        print(sentiment)
        
    st.text(sentiment)