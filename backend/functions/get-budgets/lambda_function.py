import json

from input_sanitize import *
from budget_queries import get_budgets
from errors import *

def lambda_handler(event, context):
    # Retrieve budgets given certain criteria
    # By type, date range, amount range, or all budgets 
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'name': 'str'
    #       'min_amount' : 'num' 
    #       'max_amount': 'num'
    #       'type': 'str'
    #       'start_date': 'YYYY-MM-DD' default is 2000-01-01
    #       'end_date': 'YYYY-MM-DD' default is current day
    #       'period': 'str'
    #       'is_recurring': 'bool'
    #    }
    #  } 
    try:
        fields = json.loads(event.get('body') or '{}')
        budgets = get_budgets(
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
        name = sanitize_name(fields.get('name')) if fields.get('name') else None,
        min_amount = sanitize_amount(fields.get('min_amount')) if fields.get('min_amount') else None,
        max_amount = sanitize_amount(fields.get('max_amount')) if fields.get('max_amount') else None,
        budget_type = sanitize_type(fields.get('type')) if fields.get('type') else None,
        start_date = sanitize_date(fields.get('start_date')) if fields.get('start_date') else None,
        end_date = sanitize_date(fields.get('end_date')) if fields.get('end_date') else None,
        period = sanitize_period(fields.get('period')) if fields.get('period') else None,
        is_recurring = sanitize_is_recurring(fields.get('is_recurring')) if fields.get('is_recurring') else None,
        )
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'budgets': budgets, # Need to convert from decimal to float
                'count': len(budgets)
        }, cls = DecimalEncoder)
    }
    except ValidInputError as e:
        print(f'ValidInputError: {str(e)}')
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'statusCode': 502, 'headers': headers, 'body': json.dumps({'error': 'A Database error has occurred'})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': 'Internal Server Error'})}