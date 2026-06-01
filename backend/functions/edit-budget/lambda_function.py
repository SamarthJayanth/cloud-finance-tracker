from datetime import datetime, date
import json

from input_sanitize import *
from errors import *

def lambda_handler(event: dict):
    # Edits the details of a previously made budget
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'type': 'str'
    #       'date': 'YYYY-MM-DD'
    #       'period': 'str' one of allotted types
    #       'description': 'str'
    #       'is_recurring': 'bool'
    #       'id': 'str'
    #    }
    #  } 
    try:
        fields = event.get('body')
        budget_id = fields.get('id')

        # This sends a full request, not just the changes
        budget = {
            'id' : budget_id,
            'amount' : sanitize_amount(fields.get('amount')),
            'period' : sanitize_period(fields.get('period')),
            'type' : sanitize_type(fields.get('type')),
            'date' : sanitize_date(fields.get('date')),
            'is_recurring' : sanitize_recurring(fields.get('is_recurring')),
            'description' : sanitize_description(fields.get('description')) if fields.get('description') else None
        }
       
        edit_budget(budget) # The function verifies the budget exists 
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Budget edited successfully',
                'budget_id': budget_id
            })
        }
    except NotFoundError as e:
        return {'body': json.dumps({'error': str(e)})}
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}
