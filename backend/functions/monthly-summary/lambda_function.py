import sys
import os
from datetime import date, datetime, timedelta

def lambda_handler(event: dict):
    # Returns a report of all expenses in the month
    # Maybe customize to be for any specific month
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #    }
    #  } 
    fields = event.get('body')
    end_date = date.today()
    start_date = date.today().replace(days = 1)
    expenses = retrieve_by_date_range({'start_date':start_date, 'end_date':end_date})
    amount = 0
    for expense in expenses:
        amount += expense.get('amount')