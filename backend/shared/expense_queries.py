import sys
import os

from input_sanitize import *
# Need to extract expenses from specific dates
# Extract expenses from ranges, for the month, day, above a specific amount, etc

# Event will pass the type of call
# This can be either a range of dates, after/before, above/below an amount
def get_all_expenses(fields: dict):
    pass
def get_total_expenses():
    pass
def get_expenses_filtered(fields: dict):
    # Handles any combination of type, date range, amount range
    # Replaces get_expenses_by_type_and_amount_range
    pass
def get_expenses_by_amount_range(fields: dict):
    min_amount = sanitize_amount(fields.get('min_amount'))
    max_amount = sanitize_amount(fields.get('max_amount'))
def get_expenses_by_date_range(fields: dict):
    start_date = sanitize_date(fields.get('start_date'))
    end_date = sanitize_date(fields.get('end_date'))
    return 2

earliest_date = '2000-01-01'
def get_expenses_by_type(fields: dict):
    type = sanitize_type(fields.get('type'))
    start_date = sanitize_date(fields.get('start_date')) if fields.get('start_date') else earliest_date
    end_date = sanitize_date(fields.get('end_date')) if fields.get('end_date') else str(date.today())
