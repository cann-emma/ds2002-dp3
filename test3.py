import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/zgb8ts"
sqs = boto3.client('sqs')

def get_message():
    try:
        for counter in range(0, 10, 1):
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
                for i in response["Messages"]:
                    MyMessages= {"Order": i['MessageAttributes']['order']['StringValue'],"Word": i['MessageAttributes']['word']['StringValue']}
                    print(MyMessages)
                    for x, y in MyMessages.items():
                        print(x, y)
                        Output= {x, y}
                        print(Output)
                

        else:
                print("No message in the queue")
                exit(1)
    except ClientError as e:
        print(e.response['Error']['Message'])

# Trigger the function
if __name__ == "__main__":
    get_message()


# Output= [{'order'= 5, "Word"= 'talking'}, {'order'= 9, "Word"= 'PowerPoint.'}
#     {'order'= 8, "Word"= 'need'},{'order'= 4, "Word"= 'they're'},
#     {'order'= 2, "Word"= 'know'}, {'order'= 0, "Word"= 'People'},
#      {'order'= 6, "Word"= 'about'},{'order'= 7, "Word"= 'don't'},
#      {'order'= 1, "Word"= 'who'},{'order'= 3, "Word"= 'what'}]


# for x in range(Output):
