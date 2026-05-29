import json
import sys
import os
import math
from datetime import date, datetime, timedelta
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
    try:
        fields = event.get('body')
        goal_id = fields.get('id')
        goal = get_goal(goal_id)
        start_date = goal.get('date')
        total_income = get_total_income(sanitize_date(start_date),str(date.today()))
        all_expenses = retrieve_by_date_range(sanitize_date(start_date),str(date.today()))
        total_expenses = sum(exp.get('amount', 0) for exp in all_expenses)
        percentage_to_goal = (total_income / total_expenses)
        if (percentage_to_goal > 1.00):
            # Goal reached
            return
        projected_delta_days = ((date.today()-datetime.strptime(start_date, '%Y-%m-%d')).days)/percentage_to_goal
        projected_delta_days = math.ceil(projected_delta_days)
        projected_end_date = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days = projected_delta_days)
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}