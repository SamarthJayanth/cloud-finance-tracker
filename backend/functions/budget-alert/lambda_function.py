import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../functions'))
from input_sanitize import *
from expense_queries import *
from daily_average import *

def lambda_handler(event: dict):
    fields = event.get('body')
    # Retrieve all from database
    all_budgets = {}
    for budget in all_budgets:
        pass