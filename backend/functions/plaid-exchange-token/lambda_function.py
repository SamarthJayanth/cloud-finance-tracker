import plaid
import json
from plaid.api import plaid_api
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
import boto3
import uuid
from errors import *

ssm = boto3.client('ssm')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.table('plaid-items')

def get_plaid_credentials():
    client_id = ssm.get_parameter(
        Name = '/cloud-finance-tracker/plaid/client_id',
        WithDecryption = True
    )['Parameter']['Value']
    secret = ssm.get_parameter(
        Name = '/cloud-finance-tracker/plaid/secret',
        WithDecryption = True
    )['Parameter']['Value']
    return client_id, secret

# the public token is received from Plaid Link


def lambda_handler(event, context):
    try:
        fields = json.loads(event.get('body') or '{}')
        public_token = fields.get['public_token']
        #This is the public token from the user, that was originally sent by plaid
        # We use this public token to exchange it for a secret access token to store for permanent use
        if not public_token:
            raise ValidInputError('public_token is required')
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        client_id, secret = get_plaid_credentials()
        configuration = plaid.Configuration(
                host=plaid.Environment.Sandbox,
                api_key={'clientId': client_id, 'secret': secret}
            )
        api_client = plaid.ApiClient(configuration)
        client = plaid_api.PlaidApi(api_client)
        exchange_request = ItemPublicTokenExchangeRequest(
        public_token = fields.get['public_token']
        )
        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response['access_token']
        item_id = exchange_response['item_id']
        try:
            table.put_item(Item = {
                'user_id': user_id,
                'item_id': item_id,
                'access_token': access_token,
                'record_id': str(uuid.uuid4())
            })
        except Exception as e:
            print(f'DynamoDB error: {str(e)}')
            raise DataBaseError('Failed to save linked account')
        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps({
                'message': 'Bank account linked successfully',
                'item_id': item_id
            })
        }
    except ValidInputError as e:
        print(f'ValidInputError: {str(e)}')
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'statusCode': 502, 'headers': headers, 'body': json.dumps({'error': 'A Database error has occurred'})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': 'Internal Server Error'})}
                