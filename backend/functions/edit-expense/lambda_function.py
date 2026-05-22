import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *

def lambda_handler(event: dict):
    # fields = json.loads(event.get('body')) for an API call
    fields = event.get('body')

    amount =  sanitize_amount(fields.get('amount'))
    expense_type = sanitize_type(fields.get('type'))
    date = sanitize_date(fields.get('date'))
    description = sanitize_description(fields.get('description'))
    id = fields.get('id')
    #Event body has expense id

    # Retrieve expense from database

    expense = { # This is placeholder for retreived one
        'amount':1,
        'type':'food',
        'date':'2024-01-02',
        'description':'To eat',
        'id':'a3f8c2d2-9b4e-4f7a-8c3d-1e2f5a6b7c8d'
    }
    expense['amount'] = amount
    expense['type'] = expense_type
    expense['date'] = date
    expense['description'] = description
    
    print(expense)
    
    #Save back to database
    

event = {'method':'http','body':{'type':'food','amount':'i','date':'2026-09-26','description':'N/A','id':'a3f8c2d2-9b4e-4f7a-8c3d-1e2f5a6b7c8d'}}
lambda_handler(event)