import sys
import os
import uuid
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
def lambda_handler(event: dict):
    # Adds an income to the database
    # Arguments
    # event =
    # {
    #   miscellaneous 
    #   body = 
    #       {
    #           'record_type': 'income'
    #           'amount': ''num'
    #           'name': 'str'
    #           'period': 'str' 
    #           'date': 'str
    #       }
    # }
    fields = event.get('body')
    period = sanitize_period(fields.get('period'))
    income = {
        'amount': sanitize_amount(fields.get('amount')),
        'name': sanitize_name(fields.get('name')),
        'period': period,
        'id': str(uuid.uuid4()),
        'date': sanitize_date(fields.get('date')),
        'is_recurring': (period != 'one-time')
    }
    # Save to database
