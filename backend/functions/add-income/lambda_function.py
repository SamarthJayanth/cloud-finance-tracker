import sys
import os
import uuid
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
from errors import *
def lambda_handler(event, context):
    # Adds an income to the database
    # Arguments
    # event =
    # {
    #   miscellaneous 
    #   user_id: 'str'
    #   body = 
    #       {
    #           'amount': ''num'
    #           'name': 'str'
    #           'period': 'str' 
    #           'start_date': 'str
    #           'description': 'str' optional
    #       }
    # }
    try:
        fields = event.get('body')

        period = sanitize_period(fields.get('period'), 'income')
        description = sanitize_description(fields.get('description')) if fields.get('description') else None
        income = {
            'user_id': sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
            'amount': sanitize_amount(fields.get('amount')),
            'name': sanitize_name(fields.get('name')),
            'period': period,
            'income_id': sanitize_id(str(uuid.uuid4())),
            'start_date': sanitize_date(fields.get('start_date')),
            'description': description
        }
        
        add_income(income)

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Income added successfully',
                'income_id': income.get('income_id')
            })
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        print(f'Unexpected rrror: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}
    # Save to database
