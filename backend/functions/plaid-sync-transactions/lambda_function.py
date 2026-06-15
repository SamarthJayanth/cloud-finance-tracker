import json
import boto3
import plaid
import uuid
from decimal import Decimal
from datetime import date
from botocore.exceptions import ClientError
from plaid.api import plaid_api
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from input_sanitize import *
from expense_queries import add_expense
from income_queries import add_income

dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
plaid_items_table = dynamodb.Table('plaid-items')
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

# Plaid has it's own categories
# We map those categories to the one's we have available
# Many categories are not mapped directly to the ones available
# We categorize unavailable categories as other
def get_type(category: str):
    category_map = {
    'food_and_drink': 'dining',
    'shops': 'shopping',
    'travel': 'transport',
    'transportation': 'transport',
    'entertainment': 'entertainment',
    'housing': 'housing',
    'utilities': 'utilities',
    'general_merchandise': 'shopping',
    'home_improvement': 'luxuries',
    'personal_care': 'luxuries'
    }   
    return category_map.get(category, 'other')

def lambda_handler(event, context):
    try:
        try:
            user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        except Exception as e:
            print(f'Invalid user_id: {str(e)}')
            return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Invalid request'})}
        # We use query to allow for multiple bank accounts
        try:    
            user_response = plaid_items_table.query(KeyConditionExpression = boto3.dynamodb.conditions.Key('user_id').eq(user_id))
            items = user_response.get('Items', [])
        except ClientError as e:
            print(f'DynamoDB query error: {str(e)}')
            return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': 'Failed to retrieve linked accounts'})}
        if not items:
            return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'No linked bank accounts found'})}
        try:    
            client_id, secret = get_plaid_credentials()
            configuration = plaid.Configuration(
                host=plaid.Environment.Sandbox,
                api_key={'clientId': client_id, 'secret': secret}
            )
            api_client = plaid.ApiClient(configuration)
            client = plaid_api.PlaidApi(api_client)
        except ClientError as e:
            print(f'SSM error retrieving credentials: {str(e)}')
            return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': 'Failed to initialize Plaid client'})}

        transactions = list()
        for item in items:
            try:
                cursor = item.get('cursor')
                access_token = item['access_token']
                has_more = True
                while (has_more):
                    if cursor:
                        request = TransactionsSyncRequest(
                            access_token=access_token,
                            cursor=cursor
                        )
                    else:
                        request = TransactionsSyncRequest(
                            access_token=access_token
                        )
                    response = client.transactions_sync(request)
                    transactions.extend(response['added'])
                    has_more = response['has_more']
                    cursor = response['next_cursor']
            # We have to store the cursor in order to ensure
            # that we store no duplicate transactions
            # We can also bypass this by using the transaction id
            # as a sort key/filter
                plaid_items_table.update_item(
                    Key={'user_id': user_id, 'item_id': item['item_id']},
                    UpdateExpression='SET cursor = :cursor',
                    ExpressionAttributeValues={':cursor': cursor}
                )
            except ClientError as e:
                print(f'DynamoDB error updating cursor for item {item.get("item_id")}: {str(e)}')
                continue       
            except plaid.ApiException as e:
                print(f'Plaid API error for item {item.get("item_id")}: {str(e)}')
                continue
        expenses_sync_count = 0
        incomes_sync_count = 0
        for transaction in transactions:
            try:
                amount = transaction.get('amount')
                if amount >= 0: #This is an expense
                    category_dict = transaction.get('personal_finance_category') or {}
                    primary = category_dict.get('primary')
                    if primary and primary.lower() == 'rent_and_utilities':
                        detailed = category_dict.get('detailed') or ''
                        if(detailed.lower() == 'rent_and_utilities_rent'):
                            category = 'housing'
                        else:
                            category = 'utilities'
                    elif primary:
                        category = primary.lower()
                    else:
                        category = 'other'
                    add_expense({
                        'user_id': user_id,
                        'amount': Decimal(str(amount)),
                        'type': get_type(category),
                        'date': transaction.get('date').strftime('%Y-%m-%d'),
                        'name': sanitize_name(transaction.get('name')),
                        'description': None,
                        'expense_id': str(uuid.uuid4())
                    })
                    expenses_sync_count += 1
                elif amount < 0: #This is an income
                    add_income({
                        'user_id': user_id,
                        'amount': Decimal(str(abs(amount))),
                        'start_date': transaction.get('date').strftime('%Y-%m-%d'),
                        'name': sanitize_name(transaction.get('name')),
                        'description': None,
                        'period': 'one-time',
                        'income_id': str(uuid.uuid4())
                    })
                    incomes_sync_count += 1
            except ClientError as e:
                print(f'Dynamodb error saving transaction {transaction.get("transaction_id")}: {str(e)}')
                continue
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'synced_expenses': expenses_sync_count,
                'synced_incomes': incomes_sync_count
            })
        }
    # the transactions in the response are paginated, so make multiple calls while incrementing the cursor to
    # retrieve all transactions
    except Exception as e:
        print(f'Error syncing plaid transactions: {str(e)}')
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Failed to sync transactions'})
        }