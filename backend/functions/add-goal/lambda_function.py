import json
import sys
import os
import uuid
from datetime import date, datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *

def lambda_handler(event: dict):
    # Sets a goal for a user to hit 
    # Goal is an amount saved in some time
     # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'name': 'str'
    #       'start_date': 'str'
    #       'end_date': 'str'
    #       'period': 'str'
    #    }
    #  } 
    try:
        fields = event.get('body')
        goal_id = str(uuid.uuid4())
        goal = {
            'amount' : sanitize_amount(fields.get('amount')),
            'name' : sanitize_name(fields.get('name')),
            'start_date': sanitize_date(fields.get('start_date')),
            'end_date': sanitize_date(fields.get('end_date')),
            'period': sanitize_period(fields.get('period')),
            'id': goal_id
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}
        # Save to database