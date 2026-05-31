from datetime import datetime, date
import json

from input_sanitize import *
from errors import *

def lambda_handler(event: dict):
    # Edits the details of a previously made goal
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'name': 'str'
    #       'start_date': 'YYYY-MM-DD'
    #       'end_date': 'YYYY-MM-DD'
    #       'description': 'str'
    #       'id': 'str'
    #    }
    #  } 
    try:
        fields = event.get('body')
        goal_id = fields.get('id')

        # retrieve goal from database
        # Placeholder
        goal = {'id':'abcs-43de-32co','name':'groceries','start_date':'2026-01-02', 'amount':100, 'end_date':'2026-05-20', 'description': 'N/A'}
        # This sends a full request, not just the changes
        start_date = sanitize_date(fields.get('start_date'))
        end_date = sanitize_date(fields.get('end_date'))
        goal['amount'] = sanitize_amount(fields.get('amount'))
        goal['name'] = sanitize_type(fields.get('name'))
        goal['description'] = sanitize_description(fields.get('description'))
        goal['start_date'] = start_date
        goal['end_date'] = end_date
        if (start_date > end_date):
            raise ValidInputError('Start date cannot be ahead of the end date')
        # Save to database
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        print(f'Unexpected rrror: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}
