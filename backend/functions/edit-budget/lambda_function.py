import sys
import os
from datetime import datetime, date

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *


def lambda_handler(event: dict):
    fields = event.get('body')
    budget_id = fields.get('id')
    
    # retrieve budget from database
    # Placeholder
    budget = {'id':'abcs-43de-32co','type':'groceries','period':'monthly', 'amount':100, 'date':'2026-05-20','is_recurring':True}
    # This sends a full request, not just the changes
    budget['amount'] = sanitize_amount(fields.get('amount'))
    budget['period'] = sanitize_period(fields.get('period'))
    budget['type'] = sanitize_type(fields.get('type'))
    budget['date'] = sanitize_date(fields.get('date'))
    if(type(is_recurring)!= bool):
        raise ValidInputError('Recurrence must be set to true or false')
    else:
        budget['is_recurring'] = fields.get('is_recurring')

    # Save to database

