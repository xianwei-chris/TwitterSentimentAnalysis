# TwitterSentimentAnalysis

## Current Progress
A Stremlit app in running on AWS EC2 instance
http://54.149.76.59:8501/
It allows users to input Twitter page name (Eg: Bitcoin), and will return recent tweets from that page and the sentiment score on the tweets

## Main Goal:

The Initial Goals with be more focusing on gaining software engineering skill
1) Understand API (serve and call)
2) Understand AWS ecosystem (services like EC2, Comprehend, S3 and concecpt about IAM role, user and policy)
3) Make a data webapp
4) Workflow for ML Model Serving
5) Configuration to work with remote server
6) Implement docker component
7) Implement CICD pipeline (start with github action)

Future Goal with be more on make real use of Twitter data and sentiment to make analysis either on crypto/stock market or help with doing business market research

What Has Been Done:
1. Understand available twitterAPI
2. Having a python function to get recent tweets
3. Having a python function to call AWS comprehend to get text sentiment
4. Having a fastapi backend and streamlit frontend and works with each other
5. Hosting the project on AWS EC2
6. Configured working environment on VSCode and Cloud9 to work with remote server

Project Pending:
1) make a more comprehensive visualization (more tweets shown and show analysis of sentiment)
2) add docker component
3) add CICD pipeline
4) enhance feature (include keyword searching)
5) create database (data streaming too)
6) change external connection into more readable URL