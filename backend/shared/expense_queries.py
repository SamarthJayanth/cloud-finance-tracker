import boto3
from datetime import date
from input_sanitize import *
# Need to extract expenses from specific dates
# Extract expenses from ranges, for the month, day, above a specific amount, etc

# Event will pass the type of call
# This can be either a range of dates, after/before, above/below an amount
earliest_date = '2000-01-01'
def get_expenses(start_date: str = earliest_date, end_date: str = None,
                 expense_type: str = None, min_amount: float = None, max_amount: float = None):
    # Returns list of expense records matching filters
    if end_date is None:
        end_date = str(date.today())
    pass

def get_total_expenses(start_date: str = earliest_date, end_date: str = None,
                       expense_type: str = None, min_amount: float = None, max_amount: float = None):
    # Returns single sum — just calls get_expenses and sums
    items = get_expenses(start_date, end_date, expense_type, min_amount, max_amount)
    return sum(item.get('amount') for item in items)