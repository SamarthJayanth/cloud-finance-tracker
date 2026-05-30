import json
import uuid
import sys
import os
import boto3
from decimal import Decimal # DynamoDB doesn't take float values
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
from errors import *

dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
table = dynamodb.Table('expense')
# event contains data from the API call
# Will also authenticate users

def lambda_handler(event: dict, context) :
    # Adds an expense to the database
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'type': 'str'
    #       'date': 'YYYY-MM-DD' default is 2000-01-01
    #       'description': 'str'
    #       'name': 'str'
    #    }
    #  } 

    # fields = json.loads(event.get('body')) for an API call
    try: 
        fields = event.get('body')
        amount =  sanitize_amount(fields.get('amount'))
        expense_type = sanitize_type(fields.get('type'))
        date = sanitize_date(fields.get('date'))
        description = sanitize_description(fields.get('description'))
        expense_id = str(uuid.uuid4())
        name = sanitize_name(fields.get('name'))
        expense = {
            'name': name,
            'amount': Decimal(amount),
            'type':expense_type,
            'date':date,
            'description':description,
            'id': expense_id
        }
        #Save to Database
        try:
            table.put_item(Item = expense)
        except Exception as e:
            print(f'DynamoDB error: {str(e)}')
            raise DataBaseError('Failed to save expense')
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Expense added successfully',
                'expense': expense
            })
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}
