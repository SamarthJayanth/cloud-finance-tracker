import json
import sys
import os
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))
from input_sanitize import *
from expense_queries import retrieve_by_type, retrieve_by_type_and_range
from budget_utils import *
def lambda_handler(event: dict):
    # Receives a budget and determines certain statistics
    # Ensures it is a valid budget, then determines the following:
    # How much is spent/remaining, how many days elpased/remain, etc
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'id' : 'str'
    #    }
    #  } 
    try:
        fields = event.get('body')
        budget_id = fields.get('id')

        # Retrieve budget for the certain type
        # placeholder here to simulate retrieval
        budget = {'id':'abcs-43de-32co','type':'groceries','period':'monthly', 'amount':100, 'date':'2026-05-20','is_recurring':True}
        start_date, end_date = get_current_period(budget)
        if (budget.get('type')=='any'):
            expenses = get_expenses_by_date_range({'start_date':start_date,'end_date':end_date})
        else:
            expenses = get_expenses_by_type({'start_date':start_date,'end_date':end_date,'type':(budget.get('type'))})
        amount_spent = sum(exp.get('amount', 0) for exp in expenses) # defaults to 0 instead of None

        status = calculate_budget_status(amount_spent, budget.get('amount'), start_date, end_date)
        return {
                'body': {
                    'budget_id':   budget_id,
                    'budget_name': budget.get('name'),
                    'period':      budget.get('period'),
                    'start_date':  str(start_date),
                    'end_date':    str(end_date),
                    **status
                }
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}