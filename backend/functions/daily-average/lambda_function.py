import sys
import os
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))
from input_sanitize import *
from expense_queries import *

def lambda_handler(event: dict):
    fields = event.get('body')
    end_date = date.today()
    start_date = date.today().replace(day = 1)
    delta_days = end_date - start_date
    expenses = retrieve_by_date_range({'start_date': start_date,'end_date': end_date})
    amount = 0
    for expense in expenses:
        amount += expense.get('amount')
    return round(amount/(delta_days.days + 1), 2)
lambda_handler({'body':'hi'})

    