import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/zgb8ts"
sqs = boto3.client('sqs')



# Retrieve all messages

def get_message(): 
    messages = [ ]

    try:
        for counter in range (0, 10, 1):
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
            if "Messages" in response:
                for i in response["Messages"]:
                    MyMessages= {"Order": int(i['MessageAttributes']['order']['StringValue']),"Word": i['MessageAttributes']['word']['StringValue']}
                    handle= i['ReceiptHandle']
                    print(handle)
                    # print(MyMessages)
                    # messages.append(MyMessages)
                    # Output= json.dumps(messages)
                    # print(Output)
                    # with open('data3.json', 'w', encoding='utf-8') as f:
                    #     json.dump(Output, f, ensure_ascii=False)
            else:
                print("No message in the queue")

    except ClientError as e:
        print(e.response['Error']['Message'])

if __name__ == "__main__":
    get_message()


## Store and Sort

from pymongo import MongoClient, errors
from bson.json_util import dumps
import os

MONGOPASS = os.getenv('MONGOPASS')
uri = "mongodb+srv://cluster0.pnxzwgz.mongodb.net/"
client = MongoClient(uri, username='nmagee', password=MONGOPASS, connectTimeoutMS=200, retryWrites=True)

db = client.zgb8ts
collection = db.save

with open('data3.json', 'r') as f:
    file_data = json.load(f)
    print(file_data)
     

    if isinstance(file_data, list):
        try:
            collection.insert_many(file_data)
        except Exception as e:
            print(e, "when importing into Mongo")
    else:
        try:
            collection.insert_one(file_data)
        except Exception as e:
            print(e)

mydat= db.save.find().sort("Order", 1)
for x in mydat:
    print(x["Word"])




# Delete Messages in Queue

def delete_message():
    while True:
        response = sqs.receive_message(QueueUrl=url,AttributeNames=['All'],
        MaxNumberOfMessages=10, MessageAttributeNames=['All'])  
        if "Messages" in response:
            for i in response["Messages"]:
                sqs.delete_message_batch(
                QueueUrl=url,
                ReceiptHandle= i['ReceiptHandle'])
                print("Message deleted") 
        else:
            print('Empty queue')  
            break  

if __name__ == "__main__":
    delete_message()    
