import json

from input_sanitize import *
from errors import *
from expense_queries import edit_expense
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
        description = sanitize_description(fields.get('description')) if (fields.get('description')) else None
        expense = {
            'user_id': sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
            'expense_id': expense_id,
            'name' : sanitize_name(fields.get('name')),
            'amount' :  sanitize_amount(fields.get('amount')),
            'type' : sanitize_type(fields.get('type')),
            'date' : sanitize_date(fields.get('date')),
            'description' : description
        }
        #Event body has expense id
        edit_expense(expense)

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Expense edited successfully',
                'expense': expense
            }, cls = DecimalEncoder)
        }
        
    except ValidInputError as e:
        print(f'ValidInputError: {str(e)}')
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'statusCode': 502, 'headers': headers, 'body': json.dumps({'error': 'A Database error has occurred'})}
    except NotFoundError as e:
        print(f'NotFoundError: {str(e)}')
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'A Resource not found error has occurred'})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': 'Internal Server Error'})}