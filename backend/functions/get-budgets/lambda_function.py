import json

from input_sanitize import *
from budget_queries import *

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
    #       'budget_type': 'str'
    #       'start_date': 'YYYY-MM-DD' default is 2000-01-01
    #       'end_date': 'YYYY-MM-DD' default is current day
    #       'period': 'str'
    #       'is_recurring': 'bool'
    #    }
    #  } 
    try:
        fields = json.loads(event.get('body', '{}'))
        budgets = get_budgets(
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
        name = sanitize_name(fields.get('name')) if fields.get('name') else None,
        min_amount = sanitize_amount(fields.get('min_amount')) if fields.get('min_amount') else None,
        max_amount = sanitize_amount(fields.get('max_amount')) if fields.get('max_amount') else None,
        budget_type = sanitize_type(fields.get('budget_type')) if fields.get('budget_type') else None,
        start_date = sanitize_date(fields.get('start_date')) if fields.get('start_date') else None,
        end_date = sanitize_date(fields.get('end_date')) if fields.get('end_date') else None,
        period = sanitize_period(fields.get('period')) if fields.get('period') else None,
        is_recurring = sanitize_is_recurring(fields.get('is_recurring')) if fields.get('is_recurring') else None,
        )
        return {
            'statusCode': 201,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'budgets': budgets, # Need to convert from decimal to float
                'count': len(budgets)
        }, cls = DecimalEncoder)
    }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}