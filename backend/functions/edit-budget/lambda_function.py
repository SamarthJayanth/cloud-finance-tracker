from datetime import datetime, date
import json

from input_sanitize import *
from errors import *
from budget_queries import *
def lambda_handler(event, context):
    # Edits the details of a previously made budget
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'type': 'str'
    #       'start_date': 'YYYY-MM-DD'
    #       'period': 'str' one of allotted types
    #       'description': 'str'
    #       'is_recurring': 'bool'
    #       'budget_id': 'str'
    #       'name': 'str'
    #    }
    #  } 
    try:
        fields = json.loads(event.get('body') or '{}')
        budget_id = sanitize_id(fields.get('budget_id'))

        # This sends a full request, not just the changes
        budget = {
            'user_id': sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
            'budget_id' : budget_id,
            'name' : sanitize_name(fields.get('name')),
            'amount' : sanitize_amount(fields.get('amount')),
            'period' : sanitize_period(fields.get('period')),
            'type' : sanitize_type(fields.get('type')),
            'start_date' : sanitize_date(fields.get('start_date')),
            'is_recurring' : sanitize_recurring(fields.get('is_recurring')),
            'description' : sanitize_description(fields.get('description')) if fields.get('description') else None
        }
       
        edit_budget(budget) # The function verifies the budget exists 
        return {
            'statusCode': 201,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'Budget edited successfully',
                'budget': budget
            }, cls = DecimalEncoder)
        }
    except ValidInputError as e:
        print(f'ValidInputError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'body': json.dumps({'error': 'A Database error has occurred'})}
    except NotFoundError as e:
        print(f'NotFoundError: {str(e)}')
        return {'body': json.dumps({'error': 'A Resource not found error has occurred'})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}