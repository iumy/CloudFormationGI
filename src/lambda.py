import json
def lambda_handler(event, context):
    ip_address = event['requestContext']['identity']['sourceIp']
    return {
        'body': json.dumps({"ip_address": ip_address}),
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200
    }