# Serverless Data Pipeline with Kinesis and Firehose for Snowflake

## Project Overview
This project implements a serverless data pipeline using AWS services, specifically designed to handle real-time data ingestion and transformation. The pipeline extracts data from a Postman request via Amazon API Gateway, processes it through AWS Lambda, and stores it in Amazon S3, where it can be analyzed or further processed in Snowflake using Snowpipe.

## Architecture Diagram
![Architecture Diagram](link-to-your-diagram)

## Tools and Technologies Used
- AWS Lambda
- Amazon API Gateway
- Amazon Kinesis Data Streams
- Amazon Kinesis Firehose
- Amazon S3
- Snowflake (for future analysis)
- Postman (for API testing)

## Complete Workflow

1. **AWS Root Account Setup**: 
   - Create a role for Lambda with the necessary permissions: `AmazonAPIGatewayInvokeFullAccess`, `AmazonKinesisFullAccess`, `AmazonS3FullAccess`, `CloudWatchEventsFullAccess`.

2. **Lambda Function Creation**: 
   - Create a Lambda function named `lambda-kinesis-function` to handle data ingestion from API Gateway.
   - Deploy the following code:
     ```python
     import json
     import boto3

     client = boto3.client('kinesis')

     def lambda_handler(event, context):
         data = json.dumps(event['body'])  
         client.put_record(StreamName="hellotesting", Data=data, PartitionKey="1")
         print("Data Inserted")
     ```

3. **API Gateway Setup**: 
   - Create an API Gateway and integrate it with the Lambda function using the POST method.
   - API endpoint example: `https://your-api-id.execute-api.region.amazonaws.com/dev/lambda-kinesis-function`.

4. **Testing API Gateway**: 
   - Send requests from Postman to verify that the Lambda function is triggered and check logs in CloudWatch.

5. **Kinesis Data Stream Creation**: 
   - Create a Kinesis Data Stream with the same name used in Lambda (`hellotesting`).

6. **Data Handling**: 
   - To ensure the data format is compatible with Snowflake, create a second Lambda function to transform JSON data from multiple records into a comma-separated format.

7. **Lambda Function for Transformation**: 
   - Create a second Lambda function that will process data from Kinesis Firehose.
   - Deploy the following code:
     ```python
     import json
     import boto3
     import base64

     output = []

     def lambda_handler(event, context):
         for record in event['records']:
             payload = base64.b64decode(record['data']).decode('utf-8')
             row_w_newline = payload + "\n"
             row_w_newline = base64.b64encode(row_w_newline.encode('utf-8'))
             
             output_record = {
                 'recordId': record['recordId'],
                 'result': 'Ok',
                 'data': row_w_newline
             }
             output.append(output_record)

         return {'records': output}
     ```

8. **Kinesis Firehose Setup**: 
   - Create a Kinesis Firehose delivery stream, set the source to Kinesis Stream, and enable Lambda transformation using the second Lambda function.

9. **S3 Bucket Creation**: 
   - Create an S3 bucket for the Firehose destination (e.g., `firehose-data-bucket-vighnesh`).

10. **Monitoring the Pipeline**: 
    - After setting up the entire pipeline, send requests from Postman and monitor the flow through CloudWatch. Check for logs and errors.

11. **Data Analysis**: 
    - Once data is successfully in S3, you can use Snowflake or Athena for analysis.

## Why Use Kinesis and Firehose?

While it may seem straightforward to have Lambda directly send data to an S3 bucket in real-time, doing so can lead to inefficiencies, especially when handling frequent or high-volume data streams.

**Kinesis** serves as a buffer or accumulator, storing incoming records in a queue. Instead of processing each record immediately, Kinesis accumulates data over a defined period or until a specific threshold (e.g., number of records or time interval) is met. Once this threshold is reached, Kinesis sends a batch of accumulated data to **Kinesis Firehose**.

**Kinesis Firehose** processes this batched data, performing necessary transformations (such as format changes or compression) before delivering it to **Amazon S3**. After the data reaches S3, additional processes can be triggered, such as running machine learning models, executing analytics jobs, or performing ETL operations.

### Advantages of Using Kinesis and Firehose
1. **Enhanced Efficiency:** Reduces the frequency of triggering the pipeline for individual records, streamlining the process.
2. **Scalability:** Handles high-throughput data streams and automatically scales to meet demand.
3. **Cost Optimization:** Minimizes interactions with S3 and other services, reducing I/O operations and optimizing costs.
4. **Reliability:** Ensures that data is queued until downstream services are ready to process it, enhancing system reliability.

## Conclusion
This project demonstrates a serverless data pipeline architecture using AWS services, providing a scalable, efficient, and reliable solution for real-time data ingestion and processing.
