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
    fields = event.get('body')
    budget_id = fields.get('id')

    # Retrieve budget for the certain type
    # placeholder here to simulate retrieval
    budget = {'id':'abcs-43de-32co','type':'groceries','period':'monthly', 'amount':100, 'date':'2026-05-20','is_recurring':True}
    start_date, end_date = get_current_period(budget)
    delta_time = 0
    
