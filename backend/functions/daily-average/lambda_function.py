import sys
import os
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))
from input_sanitize import *
from expense_queries import *

def lambda_handler(event: dict):
    # Calculates the daily average spending in a certain time period
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'type': 'str'
    #       'start_date': 'YYYY-MM-DD' defaults to 2000-01-01
    #       'end_date': 'YYYY-MM-DD' defaults to current day
    #    }
    #  }
    fields = event.get('body')
    start_date = sanitize_date(fields.get('start_date'))
    end_date = sanitize_date(fields.get('end_date'))
    expenses_type = sanitize_type(fields.get('type'))
    delta_days = datetime.strptime(end_date, '%Y-%m-%d').date() - datetime.strptime(start_date, '%Y-%m-%d').date()
    if(delta_days.days < 0):
        raise ValidInputError("Start date must be before end date")
    
    expenses = retrieve_by_type({'start_date': start_date, 'end_date': end_date, 'type':expenses_type})
    amount = 0
    for expense in expenses:
        amount += expense.get('amount')
    return round(amount/(delta_days.days + 1), 2)
lambda_handler({'body':{'start_date':'2026-05-20','end_date':'2026-05-22'}, 'etc':9})

    