import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../functions/daily-average'))
from input_sanitize import *
from expense_queries import *
from daily-average import * 
from get-budget-status import *

def lambda_handler(event: dict):
    # Notifies if 80% of any budget has been used
    # Also notifies if the current rate of expenses exceeds the limit set
    # Weekly gets notifs once a day, biweekly every 2 days, monthly each week, quarterly every 2 weeks, yearly each month
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       
    #    }
    #  }
    fields = event.get('body')
    # Retrieve all from database
    all_budgets = {}
    for budget in all_budgets:
        # Call budget-status
        # Check amounts returned
        pass