import json
import uuid
from datetime import date
from decimal import Decimal # DynamoDB doesn't take float values
from input_sanitize import * # comes from layer automatically
from errors import * # comes from layer automatically
from income_queries import *
from expense_queries import *



def lambda_handler(event: dict, context):
    # Returns how much has been saved in a certain period of time
    # Date is optional
    fields = event.get('body') if event.get('body') else {}
    kwargs = {}
    # Want to check if start date is non empty but also assign it
    # Also need to know which arguments to pass through, use kwargs
    if(start_date := fields.get('start_date')):
        kwargs['start_date'] = sanitize_date(start_date)
    if (end_date := fields.get('end_date')):
        kwargs['end_date'] = sanitize_date(end_date)
    total_income = get_total_income(**kwargs)
    total_expense = get_total_expenses(**kwargs)
    return {
        'body': {
            'total_savings': total_income-total_expense
        }
    }