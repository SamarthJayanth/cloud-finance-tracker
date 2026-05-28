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
        expenses = retrieve_by_date_range({'start_date':start_date, 'end_date':end_date})
        amount = 0
        for expense in expenses:
            amount += expense.get('amount')
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}