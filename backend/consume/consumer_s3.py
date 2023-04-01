import boto3
import json
from datetime import datetime, timedelta

STREAM_NAME = "ExampleInputStream"
BUCKET_NAME = "twitter-data-chris"
START_TIME = datetime(2023, 3, 27, 15, 0, 0) #utc
BATCH_INTERVAL = 60  # Batch records for every 60 seconds

kinesis_client = boto3.client("kinesis", region_name="us-east-1")
s3_client = boto3.client('s3', region_name="us-east-1")

batch = []
try:
    start_time = START_TIME
    #start_time_timestamp = int(START_TIME.timestamp())

    print(f"Getting connection, iterator and shit...")
    stream = kinesis_client.describe_stream(StreamName=STREAM_NAME) 
    shard_id = stream["StreamDescription"]["Shards"][0]["ShardId"]
    print(f"Got {shard_id=}")
    shard_iterator = kinesis_client.get_shard_iterator(
        StreamName=STREAM_NAME,
        ShardId=shard_id,
        ShardIteratorType='AT_TIMESTAMP',
        Timestamp=str(START_TIME)
    )['ShardIterator']

    print(f"Reading data...")

    response = kinesis_client.get_records(ShardIterator=shard_iterator, Limit=100)
    
    while "NextShardIterator" in response:

        if len(response['Records']) < 1:
            print("No data received")

        else:
            for record in response['Records']:
                data = json.loads(record['Data'])
                print(f"Received {data=}")
                print(f"Kinesis record timestamp: {record['ApproximateArrivalTimestamp']}")

                date_format = "%Y-%m-%dT%H:%M:%S.%f+00:00"
                event_date_time = datetime.strptime(data['event_time'], date_format) #check event date time
                print(event_date_time)
                print(start_time)

                if event_date_time < start_time + timedelta(minutes=1):
                    batch.append(data)

                # If the current time is greater than start_time + 1 minute, process the batch and reset start_time
                if event_date_time >= start_time + timedelta(minutes=1):
                    
                    if len(batch) == 0:
                        print(f'no data is found in the interval, skip saving into s3')
                        
                    elif len(batch) >= 1 :
                        strf_format = "%Y/%m/%d/%H-%M"
                        formatted_start_time = start_time.strftime(strf_format)
                        s3_key=f'stream/{STREAM_NAME}/{formatted_start_time}.json'

                        # Process the batch (write the records to S3)
                        s3_client.put_object(
                            Bucket=BUCKET_NAME,
                            Key=s3_key,
                            Body=json.dumps(batch)
                            )
                        print(f'save batch of stream data into {s3_key}')
                        print(f'number of records = {len(batch)}')

                    # Reset start_time to the start of the next minute interval
                    start_time += timedelta(minutes=1)

                    # Reset batch to an empty list
                    batch = []

        response = kinesis_client.get_records(ShardIterator=response["NextShardIterator"], Limit=100)

except KeyboardInterrupt:
    print("Finishing due to keyboard interrupt")


# if i start sending stream since 2023-03-27 15:08:00
# using trim_horizon/ at_timestamp = 2023-03-26 00:00:00, the first few iterations have no records, not sure why
# kinesis stream arrival time will be utc, and at_timestamp will be based on utc too