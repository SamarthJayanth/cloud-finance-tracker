import sys
import os
from datetime import date

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
from expense_queries import *

def lambda_handler(event: dict):
    # Retrieves a summary of expenses
    # Retrieves based on type and date
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'type': 'str'
    #       'start_date': 'YYYY-MM-DD' default is 2000-01-01
    #       'end_date': 'YYYY-MM-DD' default is current day
    #    }
    #  } 
    fields = event.get('body')
    start_date = sanitize_date(fields.get('start_date')) if fields.get('start_date') else date(2000, 1, 1)
    end_date = sanitize_date(fields.get('end_date')) if fields.get('end_date') else date.today()
    expense_type = sanitize_type(fields.get('type'))
    expenses = retrieve_by_type({'start_date':start_date,'end_date':end_date,'type':expense_type})
    return