import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *

def lambda_handler(event: dict):
    # Edits a previously added expense
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'name': 'str'
    #       'amount' : 'num' 
    #       'type': 'str'
    #       'date': 'YYYY-MM-DD'
    #       'description': 'str'
    #       'id': 'str'
    #    }
    #  } 
    # fields = json.loads(event.get('body')) for an API call
    try:    
        fields = event.get('body')
        expense_id = fields.get('id')
        expense = {
            'id': expense_id,
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
            'body': json.dumps({
                'message': 'Expense edited successfully',
                'expense_id': expense_id
            })
        }
        
        #Save back to database
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except NotFoundError as e:
        return {'statusCode': 404, 'body': json.dumps({'error': str(e)})}
    except Exception:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}
