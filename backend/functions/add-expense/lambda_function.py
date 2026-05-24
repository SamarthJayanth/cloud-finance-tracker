import json
import uuid
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *

# event contains data from the API call
# Will also authenticate users

def lambda_handler(event: dict) :
    # Adds an expense to the database
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'type': 'str'
    #       'date': 'YYYY-MM-DD' default is 2000-01-01
    #       'description': 'str'
    #    }
    #  } 

    # fields = json.loads(event.get('body')) for an API call
    fields = event.get('body')
    amount =  sanitize_amount(fields.get('amount'))
    expense_type = sanitize_type(fields.get('type'))
    date = sanitize_date(fields.get('date'))
    description = sanitize_description(fields.get('description'))
    id = str(uuid.uuid4())

    expense = {
        'amount':amount,
        'type':expense_type,
        'date':date,
        'description':description,
        'id':id
    }

    print(expense)
    # Save to DataBase


event={'method':'http','body':{'type':'food','amount':'100000000  ','date':'2026-09-26','description':'N/A'}}
lambda_handler(event)