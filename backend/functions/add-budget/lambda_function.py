import json
import sys
import os
import uuid

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
def lambda_handler(event: dict):
    # Receives input details of a specific budget from user
    # Assigns an id and stores to database
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'type': 'str'
    #       'date': 'YYYY-MM-DD' 
    #       'name': 'str'
    #       'period': 'str' one of allotted types
    #       'is_recurring': 'bool'
    #    }
    #  } 
    try:
        fields = event.get('body')
        # Set a budget, can choose what category to use for this budget
        budget_amount = sanitize_amount(fields.get('amount'))
        budget_date = sanitize_date(fields.get('date'))
        budget_period = sanitize_period(fields.get('period'))
        budget_type = sanitize_type(fields.get('type'))
        budget_name = sanitize_name(fields.get('name')) # Fix name
        budget_id = str(uuid.uuid4())
        budget_is_recurring = sanitize_recurring(fields.get('is_recurring'))
        # Type can be for a timeframe, certain expense types, etc
        budget = {
            'budget_amount' : budget_amount,
            'budget_date' : budget_date,
            'budget_period' : budget_period,
            'budget_type' : budget_type,
            'budget_name' : budget_name,
            'budget_id' : budget_id,
            'budget_is_recurring' : budget_is_recurring
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        print(f'Unexpected rrror: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}