import json
import boto3
import urllib
def lambda_handler(event, context):
    # TODO implement
    body = json.loads(event.get("body", "{}"))
    email = body.get("email", "")
    response = boto3.client('sns')
    response.subscribe(
    TopicArn='###############################################',
    Protocol='email',
    Endpoint=email
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
