from datetime import datetime, date
import json

from input_sanitize import *
from errors import *
from expense_queries import *
def lambda_handler(event, context):
    # Edits a previously added expense
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'name': 'str'
    #       'amount' : 'num' 
    #       'type': 'str'
    #       'date': 'YYYY-MM-DD'
    #       'description': 'str'
    #       'expense_id': 'str'
    #    }
    #  } 
    # fields = json.loads(event.get('body')) for an API call
    try:    
        fields = json.loads(event.get('body') or '{}')
        expense_id = sanitize_id(fields.get('expense_id'))
        expense = {
            'user_id': sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
            'expense_id': expense_id,
            'name' : sanitize_name(fields.get('name')),
            'amount' :  sanitize_amount(fields.get('amount')),
            'type' : sanitize_type(fields.get('type')),
            'date' : sanitize_date(fields.get('date')),
            'description' : sanitize_description(fields.get('description'))
        }
        #Event body has expense id
        edit_expense(expense)

        return {
            'statusCode': 201,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'Expense edited successfully',
                'expense': expense
            }, cls = DecimalEncoder)
        }
        
    except ValidInputError as e:
        print(f'ValidInputError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except NotFoundError as e:
        print(f'NotFoundError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}