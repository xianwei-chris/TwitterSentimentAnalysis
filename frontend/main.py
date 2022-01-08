# frontend/main.py

import requests
import streamlit as st

# defines an h1 header
st.title("Tweets Sentiment")

# displays a file uploader widget
keyword = st.text_area("Input page name keyword")
data = {'pagename':keyword}

# displays a button
if st.button("Get Sentiment"):
    if keyword:

        res = requests.post(f"http://0.0.0.0:8080/", json=data)
        #res = requests.post(f"http://backend:8080/", json=data)
        sentiment = res.json()
        print(sentiment)