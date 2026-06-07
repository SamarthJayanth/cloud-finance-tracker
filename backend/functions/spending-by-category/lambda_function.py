import json
from datetime import date

from input_sanitize import *
from expense_queries import *

def lambda_handler(event, context):
    pass
    # Retrieves a summary of expenses
    # Retrieves based on type and date
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'start_date': 'YYYY-MM-DD' default is 2000-01-01
    #       'end_date': 'YYYY-MM-DD' default is current day
    #    }
    #  } 
    try:
        fields = json.loads(event.get('body') or '{}')
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        start_date = sanitize_date(fields.get('start_date')) if fields.get('start_date') else str(date(2000, 1, 1))
        end_date = sanitize_date(fields.get('end_date')) if fields.get('end_date') else str(date.today())
        allowed_types = {'groceries', 'transport', 'utilities', 'shopping', 'housing', 'entertainment', 'luxuries', 'dining', 'any'}
        val_to_return = list()
        for category in allowed_types:
            val_to_return.append({'category': category, 'total': get_total_expenses(user_id = user_id, start_date = start_date, end_date = end_date, expense_type = category)})
        return {
            'statusCode': 201,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'categories': val_to_return 
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