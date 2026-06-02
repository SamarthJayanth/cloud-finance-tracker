import sys
import os
import uuid
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
from errors import *
def lambda_handler(event: dict):
    # Adds an income to the database
    # Arguments
    # event =
    # {
    #   miscellaneous 
    #   body = 
    #       {
    #           'record_type': 'income'
    #           'amount': ''num'
    #           'name': 'str'
    #           'period': 'str' optional
    #           'date': 'str
    #       }
    # }
    try:
        fields = event.get('body')

        period = sanitize_period(fields.get('period'))
        description = sanitize_description(fields.get('description')) if fields.get('description') else None
        income = {
            'amount': sanitize_amount(fields.get('amount')),
            'name': sanitize_name(fields.get('name')),
            'period': period,
            'id': str(uuid.uuid4()),
            'start_date': sanitize_date(fields.get('date')),
            'description': description
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        print(f'Unexpected rrror: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}
    # Save to database
