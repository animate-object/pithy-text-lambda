import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import logging
from uuid import uuid4
from json import dumps


def lambda_handler(event, context):
    try:
        logging.debug('connecting to dynamo')
        dy = boto3.resource('dynamodb', region_name='us-east-1')
        table = dy.Table('pithy-text')
        return {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': dumps(get_random_text(table))
        }
    except LambdaException as le:
        return {
            'functionError': le.args[0],
            'statusCode': le.status_code
        }
    except Exception as e:
        logging.exception('Lambda failed unexpectedly')
        return {
            'functionError': 'Service failed unexpectedly',
            'statusCode': 500
        }


def get_random_text(table, retry_id=None):
    """Get a random entry from the pithy texst table, single retry
    Leverage sort key conditions to get nearest key to a random uuid
    """
    try:
        random_uuid = str(uuid4()) if not retry_id else retry_id
        hk_condition = Key('ph').eq(0)  # for now we are only leverageing sort key to randomize our selection
        sk_condition = Key('id').gt(random_uuid) if not retry_id else Key('id').lt(random_uuid)
        response = table.query(KeyConditionExpression=hk_condition & sk_condition, Limit=1)['Items'][0]
        return {'firstLine': response['firstLine'], 'secondLine': response['secondLine']}

    except IndexError:
        if retry_id:
            raise LambdaException('No pithy text found', 404) 
        else:
            logging.info('Missed random entry, retrying')
            return get_random_text(table, retry_id=random_uuid)


class LambdaException(Exception):
    def __init__(self, message, status_code):
        super(LambdaException, self).__init__(message)
        self.status_code = status_code

