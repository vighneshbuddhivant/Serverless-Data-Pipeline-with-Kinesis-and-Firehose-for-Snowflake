import json
import boto3

client = boto3.client('kinesis')

def lambda_handler(event, context):
    data = json.dumps(event['body'])  
    client.put_record(StreamName="hellotesting", Data=data, PartitionKey="1")
    print("Data Inserted")