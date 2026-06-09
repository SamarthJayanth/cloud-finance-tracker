import json
from datetime import date

from input_sanitize import *
from expense_queries import get_total_expenses
from income_queries import get_total_income
from errors import *
def lambda_handler(event, context):
    # Returns a report of all expenses in the month
    # Maybe customize to be for any specific month
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #    }
    #  } 
    try:
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        end_date = str(date.today())
        start_date = str(date.today().replace(day = 1))
        total_expenses = get_total_expenses(user_id = user_id,start_date = start_date, end_date = end_date)
        total_income = get_total_income(user_id = user_id, start_date = start_date, end_date = end_date)
        return {
            'statusCode': 201,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'month': date.today().strftime('%B %Y'),
                'total_income': total_income,
                'total_expenses': total_expenses,
                'amount_saved': round(total_income - total_expenses, 2)
            }, cls = DecimalEncoder)
        }
    except ValidInputError as e:
        print(f'ValidInputError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'body': json.dumps({'error': 'A Database error has occurred'})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}