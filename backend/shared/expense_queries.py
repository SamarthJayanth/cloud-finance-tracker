import sys
import os

from input_sanitize import *
# Need to extract expenses from specific dates
# Extract expenses from ranges, for the month, day, above a specific amount, etc

# Event will pass the type of call
# This can be either a range of dates, after/before, above/below an amount
def retrieve_all(fields: dict):
    pass
def retrieve_by_type_and_amount_range(fields: dict):
    pass
def retrieve_by_amount_range(fields: dict):
    amount = sanitize_amount(fields.get('amount'))

def retrieve_by_date_range(fields: dict):
    start_date = sanitize_date(fields.get('start_date'))
    end_date = sanitize_date(fields.get('end_date'))

def retrieve_by_type(fields: dict):
    type = sanitize_type(fields.get('type'))

def retrieve_by_type_and_date_range(fields: dict):
    type = sanitize_type(fields.get('type'))
    start_date = sanitize_date(fields.get('start_date'))
    end_date = sanitize_date(fields.get('end_date'))