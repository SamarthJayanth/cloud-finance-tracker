import sys
import os
from datetime import date, datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *

def lambda_handler(event: dict):
    # Sets a goal for a user to hit 
    # Goal is an amount saved in some time
     # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'name': 'str'
    #       'date': 'str'
    #       'period': 'str'
    #    }
    #  } 
    fields = event.get('body')
    goal = {
        'amount' : sanitize_amount(fields.get('amount')),
        'name' : sanitize_name(fields.get('name')),
        'date': sanitize_date(fields.get('date')),
        'period': sanitize_period(fields.get('period'))
    }
    # Save to database