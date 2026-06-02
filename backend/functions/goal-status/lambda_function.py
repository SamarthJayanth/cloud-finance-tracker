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
from goal_utils import *
from income_queries import *

def lambda_handler(event, context):
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
        goal = get_goal_by_id(goal_id)
        goal_amount = goal.get('amount')
        start_date = goal.get('start_date')
        end_date = goal.get('end_date')
        total_income = get_total_incomes(sanitize_date(start_date), str(date.today()))
        total_expense = get_total_expenses(sanitize_date(start_date), str(date.today()))
        status = calculate_goal_status(amount_spent = total_expense, income_earned = total_income, target_savings = goal_amount, start_date = start_date, end_date = end_date)
        return {
            'body': {
                    'id':   goal_id,
                    'name': goal.get('name'),
                    'start_date':  start_date,
                    'end_date':    end_date,
                    'description': goal.get('description')
                    **status
                }
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}