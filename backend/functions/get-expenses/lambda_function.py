import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
# Need to extract expenses from specific dates
# Extract expenses from ranges, for the month, day, above a specific amount, etc

# Event will pass the type of call
# This can be either a range of dates, after/before, above/below an amount
def retrieve_above_amount(fields: dict):
    amount = sanitize_amount(fields.get('amount'))
    # Retrieve with the condition that > amount

def retrieve_below_amount(fields: dict):
    amount = sanitize_amount(fields.get('amount'))

def retrieve_after_date(fields: dict):
    start_date = sanitize_date(fields.get('date'))

def retrieve_before_date(fields: dict):
    end_date = sanitize_date(fields.get('date'))
    # Retrieve with the condition that > date
def retrieve_in_date_range(fields: dict):
    start_date = sanitize_date(fields.get('start_date'))
    end_date = sanitize_date(fields.get('end_date'))
def retrieve_by_type(fields: dict):
    type = sanitize_type(fields.get('type'))
def retrieve_by_type_and_range(fields: dict):
    type = sanitize_type(fields.get('type'))
    start_date = sanitize_date(fields.get('start_date'))
    end_date = sanitize_date(fields.get('end_date'))
def lambda_handler(event: dict):
    fields = event.get('body')
    get_type = fields.get('type')
    match get_type: 
        case'above_amount':
            retrieve_above_amount(fields)
        case'below_amount':
            retrieve_below_amount(fields)
        case'after_date':
            retrieve_after_date(fields)
        case'before_date':
            retrieve_before_date(fields)
        case'in_date_range':
            retrieve_in_date_range(fields)
        case 'type':
            retrieve_by_type(fields)
        case 'type_and_in__range':
            retrieve_by_type_and_range(fields)