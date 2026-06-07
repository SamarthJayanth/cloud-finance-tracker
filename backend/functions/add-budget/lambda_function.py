import json
import uuid

from input_sanitize import *
from errors import *
from budget_queries import *
def lambda_handler(event, context):
    # Receives input details of a specific budget from user
    # Assigns an id and stores to database
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #   user_id: 'str'
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'type': 'str'
    #       'start_date': 'YYYY-MM-DD' 
    #       'name': 'str'
    #       'period': 'str' one of allotted types
    #       'is_recurring': 'bool'
    #       'description': 'str' optional
    #    }
    #  } 
    try:
        fields = json.loads(event.get('body') or '{}')
        # Set a budget, can choose what category to use for this budget
        # Type can be for a timeframe, certain expense types, etc
        description = sanitize_description(fields.get('description')) if fields.get('description') else None
        budget = {
            'user_id': sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
            'amount' : sanitize_amount(fields.get('amount')),
            'start_date' : sanitize_date(fields.get('start_date')),
            'period' : sanitize_period(fields.get('period')),
            'type' : sanitize_type(fields.get('type')),
            'name' : sanitize_name(fields.get('name')),
            'budget_id' : sanitize_id(str(uuid.uuid4())),
            'is_recurring' : sanitize_recurring(fields.get('is_recurring')),
            'description': description
        }
        add_budget(budget)
        return {
            'statusCode': 201,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'Budget added successfully',
                'budget_id': budget.get('budget_id')
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