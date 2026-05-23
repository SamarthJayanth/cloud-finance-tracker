import sys
import os
from datetime import date, datetime, timedelta

def lambda_handler(event: dict):
    fields = event.get('body')
    end_date = date.today()
    start_date = date.today() - timedelta(days=30)
    expenses = retrieve_by_data_range({'start_date':start_date, 'end_date':end_date})
    amount = 0
    for expense in expenses:
        amount += expense.get('amount')
    return amount