import plaid
from plaid.api import plaid_api
import boto3
import json
from input_sanitize import sanitize_id
from errors import *
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products

# Available environments are
# 'Production'
# 'Sandbox'

ssm = boto3.client('ssm')

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




def lambda_handler(event, context):
    try:    
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        client_id, secret = get_plaid_credentials()

        # This is from Plaid's documentation/examples
        # The server must create a link token to send to user
        # In order to allow the user to set up Plaid Link

        configuration = plaid.Configuration(
        host=plaid.Environment.Sandbox,
        api_key={
            'clientId': client_id,
            'secret': secret,
            }
        )
        api_client = plaid.ApiClient(configuration)
        client = plaid_api.PlaidApi(api_client)
        request = LinkTokenCreateRequest(
        products=[Products('transactions')],
        client_name='Cloud Finance Tracker',
        country_codes=[CountryCode('US')],
        language="en",
        user=LinkTokenCreateRequestUser(client_user_id=user_id),
        )
        response = client.link_token_create(request)
        # Must send the link token to the user
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({'link_token': response['link_token']})
        }
    except AppError as e:
        return {'statusCode': 400, 'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}, 'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'statusCode': 500, 'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'Internal Server Error'})}
