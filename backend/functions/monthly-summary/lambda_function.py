import json
from datetime import date, datetime, timedelta

from input_sanitize import *
from expense_queries import *
from income_queries import *
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
        fields = event.get('body')
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        end_date = str(date.today())
        start_date = str(date.today().replace(day = 1))
        total_expenses = get_total_expenses(user_id = user_id,start_date = start_date, end_date = end_date)
        total_income = get_total_income(user_id = user_id, start_date = start_date, end_date = end_date)
        return {
            'body': json.dumps({
                'month': date.today().month,
                'amount_spent': total_expenses,
                'amount_earned': total_income,
                'amount_saved': round(total_income - total_expenses, 2) if total_income > total_expenses else 0
            }, cls = DecimalEncoder)
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}