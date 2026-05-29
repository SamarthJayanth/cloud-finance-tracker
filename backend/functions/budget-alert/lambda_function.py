import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))
from budget_utils import *
from input_sanitize import *
from expense_queries import *


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
    try:
        fields = event.get('body')
        # Retrieve all from database
        all_budgets = set()
        for budget in all_budgets:
            # Call budget-status
            # Check amounts returned
            start_date, end_date = get_current_period(budget)
            expenses = retrieve_by_date_range({'start_date':start_date, 'end_date': end_date})
            amount_spent = sum(exp.get('amount', 0) for exp in expenses)
            full_status = calculate_budget_status(amount_spent, budget.get('amount', 0), start_date, end_date)
            if (full_status.get('status') == 'warning'):
                pass #Send alert
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}