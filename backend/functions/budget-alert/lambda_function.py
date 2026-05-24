import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../functions'))
from input_sanitize import *
from expense_queries import *
from daily_average import *

def lambda_handler(event: dict):
    # Notifies if 80% of any budget has been used
    # Also notifies if the current rate of expenses exceeds the limit set
    # Can set the rate of notifications too, for exmample a weekly notification, daily, etc
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
        pass