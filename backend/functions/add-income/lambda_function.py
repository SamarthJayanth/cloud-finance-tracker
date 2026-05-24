import sys
import os

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
    #       }
    # }
    fields = event.get('body')
    income = {
        'amount': sanitize_amount(fields.get('amount')),
        'name': sanitize_name(fields.get('name')),
        'period': sanitize_period(fields.get('period'))
    }
    # Save to database
