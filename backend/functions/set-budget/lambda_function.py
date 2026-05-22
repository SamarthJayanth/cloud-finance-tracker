import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
def lambda_handler(event: dict):
    fields = event.get('body')
    # Set a budget, can choose what category to use for this budget
    budget_amount = sanitize_amount(fields.get('amount'))
    budget_date = sanitize_date(fields.get('date'))
    budget_period = sanitize_type(fields.get('period'))
    budget_type = sanitize_type(fields.get('type'))
    budget_name = sanitize_type(fields.get('name'))
    # Type can be for a timeframe, certain expense types, etc
    # Save to database, maybe include an id?
    