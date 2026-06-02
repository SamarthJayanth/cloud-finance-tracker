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
    start_date = fields.get('start_date') 
    end_date = fields.get('end_date')
    if(start_date and end_date):
        total_income = get_total_income(start_date = sanitize_date(start_date), end_date = sanitize_date(end_date))
        total_expense = get_total_expenses(start_date = sanitize_date(start_date), end_date = sanitize_date(end_date))
    elif(start_date and not end_date):
        total_income = get_total_income(start_date = sanitize_date(start_date))
        total_expense = get_total_expenses(start_date = sanitize_date(start_date))
    elif(end_date and not end_date):
        total_income = get_total_income(end_date = sanitize_date(end_date))
        total_expense = get_total_expenses(end_date = sanitize_date(end_date))
    else:
        total_income = get_total_income()
        total_expense = get_total_expenses()
    return {
        'body': {
            'total_savings': total_income-total_expense
        }
    }