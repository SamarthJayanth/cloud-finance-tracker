import json
import sys
import os
from datetime import date, datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
from expense_queries import *
def lambda_handler(event: dict):
    # Returns a report of all expenses in the month
    # Maybe customize to be for any specific month
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #    }
    #  } 
    try:
        fields = event.get('body')
        end_date = date.today()
        start_date = date.today().replace(day = 1)
        total_expenses = get_total_expenses(start_date = start_date, end_date = end_date)
        total_income = get_total_income(start_date = start_date, end_date = end_date)
        return {
            'body': {
                'amount_spent': total_expenses,
                'amount_earned': total_income,
                'amount_saved': round(total_income - total_expenses, 2) if total_income > total_expenses else 0
            }
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}