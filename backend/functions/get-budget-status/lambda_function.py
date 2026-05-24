import sys
import os
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))
from input_sanitize import *
sys.path.append(os.path.join(os.path.dirname(__file__), '../get_expenses'))
from expense_queries import retrieve_by_type, retrieve_by_type_and_range
from get_expenses import *
def lambda_handler(event: dict):
    fields = event.get('body')
    budget_id = fields.get('id')

    # Retrieve budget for the certain type
    # placeholder here to simulate retrieval
    budget = {'id':'abcs-43de-32co','type':'groceries','period':'monthly', 'amount':100, 'date':'2026-05-20','is_recurring':True}

    budget_type = budget.get('type')
    budget_amount = budget.get('amount')
    budget_period = budget.get('period')
    budget_date = budget.get('date')
    delta_time = 0
    which_time = ''
    match budget_period:
        case 'weekly':
            delta_time = 1
            which_time = 'weeks'
        case  'biweekly':
            delta_time = 2
            which_time = 'weeks'
        case 'monthly':
            delta_time = 1
            which_time = 'months'
        case 'quarterly':
            delta_time = 3
            which_time = 'months'
        case 'yearly':
            delta_time = 1
            which_time = 'years'
    # Maybe can be written more efficiently
    if (budget.get('is_recurring')):
        start_date = datetime.strptime(budget_date, '%Y-%m-%d').date()
        end_date = start_date
        match which_time:
            case 'weeks':
                while(start_date + relativedelta(weeks = delta_time) <= date.today()):
                    start_date = start_date + relativedelta(weeks = delta_time)
                end_date = start_date + relativedelta(weeks = delta_time)
            case 'months':
                while(start_date + relativedelta(months = delta_time) <= date.today()):
                    start_date = start_date + relativedelta(months = delta_time)
                end_date = start_date + relativedelta(months = delta_time)
            case 'years':
                while(start_date + relativedelta(years = delta_time) <= date.today()):
                    start_date = start_date + relativedelta(years = delta_time)
                end_date = start_date + relativedelta(years = delta_time)    
        end_date = end_date - timedelta(days = 1) #Should end on the day before
    else:
        match which_time:
            case 'weeks':
                if(start_date + relativedelta(weeks = delta_time) <= date.today()):
                    raise ValidInputError('Budget is set too far back')
                else:
                    end_date = start_date + relativedelta(weeks = delta_time) - timedelta(days = 1)
            case 'months':
                if(start_date + relativedelta(months = delta_time) <= date.today()):
                    raise ValidInputError('Budget is set too far back')
                else:
                    end_date = start_date + relativedelta(months = delta_time) - timedelta(days = 1)
            case 'years':
                if(start_date + relativedelta(years = delta_time) <= date.today()):
                    raise ValidInputError('Budget is set too far back')
                else:
                    end_date = start_date + relativedelta(years = delta_time) - timedelta(days = 1)
    
