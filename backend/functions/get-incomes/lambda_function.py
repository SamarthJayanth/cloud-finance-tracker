import json

from input_sanitize import *
from income_queries import get_incomes
from errors import *

def lambda_handler(event, context):
    # Retrieve goals given certain criteria
    # By type, date range, amount range, or all goals 
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'min_amount' : 'num' 
    #       'max_amount': 'num'
    #       'start_date': 'YYYY-MM-DD' default is 2000-01-01
    #       'end_date': 'YYYY-MM-DD' default is current day
    #       'period': 'str'
    #       'name': 'str'
    #    }
    #  } 
    try:
        fields = json.loads(event.get('body') or '{}')
        incomes = get_incomes(
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
        name = sanitize_name(fields.get('name')) if fields.get('name') else None,
        min_amount = sanitize_amount(fields.get('min_amount')) if fields.get('min_amount') else None,
        max_amount = sanitize_amount(fields.get('max_amount')) if fields.get('max_amount') else None,
        start_date = sanitize_date(fields.get('start_date')) if fields.get('start_date') else None,
        end_date = sanitize_date(fields.get('end_date')) if fields.get('end_date') else None,
        period = sanitize_period(fields.get('period')) if fields.get('period') else None
        )
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
            'incomes': incomes, # Need to convert from decimal to float
            'count': len(incomes)
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