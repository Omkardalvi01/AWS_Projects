import json
import boto3
import urllib.parse 

def lambda_handler(event, context):
    # TODO implement
    body = json.loads(event.get('body', '{}'))
    msg = body.get('msg', 'No message')
    sender = boto3.client('sns')
    sender.publish(
        TopicArn = '######################################',
        Message = msg
    )
    return {
        'statusCode': 200,
        'body': json.dumps("Success")
    }
