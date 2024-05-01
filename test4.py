import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/zgb8ts"
sqs = boto3.client('sqs')


# (1) retrieve all messages; (2) store message data; (3) reassemble the phrase from the message content

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
                    MyMessages= {"Order": i['MessageAttributes']['order']['StringValue'],"Word": i['MessageAttributes']['word']['StringValue']}
                    messages.append(MyMessages)
                    Output= json.dumps(messages, indent=2)
                    print(Output)
                    with open('data.json', 'w', encoding='utf-8') as f:
                        json.dump(Output, f, indent= 2 , ensure_ascii=False)
            else:
                print("No message in the queue")

    except ClientError as e:
        print(e.response['Error']['Message'])

if __name__ == "__main__":
    get_message()


#  delete the messages in a single execution

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])







# from pymongo import MongoClient, errors
# from bson.json_util import dumps
# import os

# MONGOPASS = os.getenv('MONGOPASS')
# uri = "mongodb+srv://cluster0.pnxzwgz.mongodb.net/"
# client = MongoClient(uri, username='nmagee', password=MONGOPASS, connectTimeoutMS=200, retryWrites=True)
# # specify a database
# db = client.zgb8ts
# # specify a collection
# collection = db.save

# with open('dat2.json', 'r') as f:
#     try:
#       file_data = json.load(f)
#     except Exception as e:
#       print(e, "error when loading", f)
     
# # Inserting the loaded data in the collection
# # if JSON contains data more than one entry
# # insert_many is used else insert_one is used
#     if isinstance(file_data, list):
#       try:
#         collection.insert_many(file_data)
#       except Exception as e:
#         print(e, "when importing into Mongo")
#     else:
#       try:
#         collection.insert_one(file_data)
#       except Exception as e:
#         print(e)

# # record= db.save.find_one({'Order': '1'})
# # print(dumps(record, indent=2))

