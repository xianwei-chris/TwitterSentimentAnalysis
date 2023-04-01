export PYTHONPATH="${PYTHONPATH}:/Users/xtan/Documents/project/TwitterSentimentAnalysis"

aws kinesis create-stream \                                                             
--stream-name ExampleInputStream \ 
--shard-count 1 \
--region us-east-1

python backend/ingestion/ingest.py
python backend/consume/consumer_s3.py