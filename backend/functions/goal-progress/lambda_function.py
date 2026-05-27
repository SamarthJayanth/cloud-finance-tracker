import sys
import os
import math
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
from expense_queries import *
from goal_queries import *
from income_queries import *

def lambda_handler(event: dict):
    # Returns total progress statistics to a savings goal
    # Arguments:
    # event = 
    # {
    #   misc
    #   body =
    #   {
    #       'id': 'str'
    #   }
    # }
    fields = event.get('body')
    goal_id = fields.get('id')
    goal = get_goal(goal_id)
    start_date = goal.get('date')
    total_income = get_total_income(sanitize_date(start_date),str(date.today()))
    total_expenses = retrieve_by_date_range(sanitize_date(start_date),str(date.today()))
    percentage_to_goal = (total_income / total_expenses)
    if (percentage_to_goal > 1.00):
        # Goal reached
        return
    projected_delta_days = ((date.today()-datetime.strptime(start_date, '%Y-%m-%d')).days())/percentage_to_goal
    projected_delta_days = math.ceil(projected_delta_days)
    projected_end_date = datetime.strptime(start_date, '%Y-%m-%d') + projected_delta_days
    