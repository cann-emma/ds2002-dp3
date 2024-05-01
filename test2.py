import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/zgb8ts"
sqs = boto3.client('sqs')

def get_message():
    try:
        while True:
            response = sqs.receive_message(
            QueueUrl=url,
            AttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ]
            )
        # Check if there is a message in the queue or not
            if "Messages" in response:
            # extract the two message attributes you want to use as variables
            # extract the handle for deletion later
                for i in response["Messages"]:
                    order= i[0]['MessageAttributes']['order']['StringValue']
                    word = i[0]['MessageAttributes']['word']['StringValue']
                    print(f"Order: {order}")
                    print(f"Word: {word}")
            else:
                print("No message in the queue")
                exit(1)
    except ClientError as e:
        print(e.response['Error']['Message'])

if __name__ == "__main__":
    get_message()