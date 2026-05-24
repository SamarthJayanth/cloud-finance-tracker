import sys
import os
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))
from input_sanitize import *
from expense_queries import *
# Daily average in a certain time period
def lambda_handler(event: dict):
    fields = event.get('body')
    start_date = sanitize_date(fields.get('start_date'))
    end_date = sanitize_date(fields.get('end_date'))
    delta_days = datetime.strptime(end_date, '%Y-%m-%d').date() - datetime.strptime(start_date, '%Y-%m-%d').date()
    if(delta_days.days < 0):
        raise ValidInputError("Start date must be before end date")
    
    expenses = retrieve_by_date_range({'start_date': start_date,'end_date': end_date})
    amount = 0
    for expense in expenses:
        amount += expense.get('amount')
    return round(amount/(delta_days.days + 1), 2)
lambda_handler({'body':{'start_date':'2026-05-20','end_date':'2026-05-22'}, '77':9})

    