from datetime import datetime, date
import json

from input_sanitize import *
from errors import *
from income_queries import *

def lambda_handler(event, context):
    # Edits the details of a previously made income
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'name': 'str'
    #       'start_date': 'YYYY-MM-DD'
    #       'period': 'str' one of allotted types
    #       'description': 'str'
    #       'income_id': 'str'
    #    }
    #  } 
    try:
        fields = json.loads(event.get('body') or '{}')
        income_id = sanitize_id(fields.get('income_id'))

        income = {
            'user_id': sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
            'income_id' : income_id,
            'amount' : sanitize_amount(fields.get('amount')),
            'period' : sanitize_period(fields.get('period'), 'income'),
            'name' : sanitize_name(fields.get('name')),
            'start_date' : sanitize_date(fields.get('start_date')),
            'description': sanitize_description(fields.get('description'))
        }

        edit_income(income)
        return {
            'statusCode': 201,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'Income edited successfully',
                'income': income
            }, cls = DecimalEncoder)
        }
        
        #Save back to database
    except ValidInputError as e:
        print(f'ValidInputError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except NotFoundError as e:
        print(f'NotFoundError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}