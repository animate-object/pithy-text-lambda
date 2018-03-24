import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import logging
from uuid import uuid4
from json import dumps

def lambda_handler(event, context):
    logging.debug('connecting to dynamo')
    dy = boto3.resource('dynamodb', region_name='us-east-1')
    table = dy.Table('pithy-text')
    return {
        'body': dumps(get_random_text(table)),
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {}
    }
def get_random_text(table, retry_id=None):
    try:
        random_uuid = str(uuid4()) if not retry_id else retry_id
        hk_condition = Key('ph').eq(0)  # for now we are only leverageing sort key to randomize our selection
        sk_condition = Key('id').gt(random_uuid) if not retry_id else Key('id').lt(random_uuid)
        response = table.query(KeyConditionExpression=hk_condition & sk_condition, Limit=1)['Items'][0]
        return {'firstLine': response['firstLine'], 'secondLine': response['secondLine']}

    except IndexError:
        if retry_id:
            return {'Status': 404, 'FunctionError': 'Nothing to say :('}
        else:
            logging.info('Missed random entry, retrying')
            return get_random_text(table, retry_id=random_uuid)
    except ClientError as ce:
        logging.exception('Uh oh')
        return {'Status': 500, 'FunctionError': 'Something went wrong'}
