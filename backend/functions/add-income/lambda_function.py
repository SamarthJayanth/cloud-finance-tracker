import uuid
import json

from input_sanitize import *
from errors import *
from income_queries import *
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
        fields = json.loads(event.get('body') or '{}')

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
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'Income added successfully',
                'income_id': income.get('income_id')
            }, cls = DecimalEncoder)
        }
    except ValidInputError as e:
        print(f'ValidInputError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}