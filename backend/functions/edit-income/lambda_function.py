from datetime import datetime, date
import json

from input_sanitize import *
from errors import *

def lambda_handler(event: dict):
    # Edits the details of a previously made income
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'name': 'str'
    #       'start_date': 'YYYY-MM-DD'
    #       'period': 'str' one of allotted types
    #       'description': 'str'
    #       'is_recurring': 'bool'
    #       'id': 'str'
    #    }
    #  } 
    try:
        fields = event.get('body')
        budget_id = fields.get('id')

        # retrieve budget from database
        # Placeholder
        income = {'id':'abcs-43de-32co','name':'work','period':'monthly', 'amount':100, 'start_date':'2026-05-20','is_recurring':True, 'description': 'some'}
        # This sends a full request, not just the changes
        income['amount'] = sanitize_amount(fields.get('amount'))
        income['period'] = sanitize_period(fields.get('period'))
        income['name'] = sanitize_type(fields.get('type'))
        income['start_date'] = sanitize_date(fields.get('date'))
        income['is_recurring'] = sanitize_recurring(fields.get('is_recurring'))
        # Save to database
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        print(f'Unexpected rrror: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}
