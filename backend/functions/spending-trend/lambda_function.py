import json
from datetime import date
from dateutil.relativedelta import relativedelta

from input_sanitize import *
from expense_queries import get_total_expenses
from errors import *

def lambda_handler(event, context):
    # Retrieves expenses per month for the past 6 month time span
    # Returns each month and total expenses
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #  } 
    try:
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        date_today = date.today()
        first_day = date_today.replace(day = 1)
        summary = list()
        for i in range(5, -1, -1):
            start = first_day - relativedelta(months = i)
            summary.append(
                {
                'month': start.strftime('%B %Y'), 
                'total': get_total_expenses(
            user_id = user_id, 
            start_date = str(start),
            end_date = str(start + relativedelta(months = 1) - relativedelta(days = 1))
            )
            })
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'spending_trend': summary
            }, cls = DecimalEncoder)
        }
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'statusCode': 502, 'headers': headers, 'body': json.dumps({'error': 'A Database error has occurred'})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': 'Internal Server Error'})}