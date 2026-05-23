import sys
import os
from datetime import date

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
from expense_queries import *

def lambda_handler(event: dict):
    fields = event.get('body')
    start_date = sanitize_date(fields.get('start_date'))
    end_date = date.today()
    expense_type = sanitize_type(fields.get('type'))
    expenses = retrieve_by_type({'start_date':start_date,'end_date':end_date,'type':expense_type})
