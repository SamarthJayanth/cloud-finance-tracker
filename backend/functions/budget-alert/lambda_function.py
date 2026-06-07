import json

from budget_utils import *
from input_sanitize import *
from expense_queries import *
from budget_queries import *

def lambda_handler(event, context):
    # Notifies if 80% of any budget has been used
    # Also notifies if the current rate of expenses exceeds the limit set
    # Weekly gets notifs once a day, biweekly every 2 days, monthly each week, quarterly every 2 weeks, yearly each month
    # Arguments:
    # event = 
    # {
    #    user_id: 'str'
    #    miscellaneous
    # body = 
    #   {
    #       
    #    }
    #  }
    try:
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        # Retrieve all from database
        all_budgets = get_budgets(user_id = user_id)
        all_budgets_alerts = {}
        for budget in all_budgets:
            # Call budget-status
            # Check amounts returned
            start_date, end_date = get_current_period(budget)
            total_expenses = float(get_total_expenses(user_id = user_id, start_date = start_date, end_date = end_date))
            full_status = calculate_budget_status(total_expenses, budget.get('amount', 0), start_date, end_date)
            all_budgets_alerts[budget.get('budget_id')] = full_status.get('status')
            if (full_status.get('status') == 'warning'):
                pass #Send alert
            return {
                'statusCode': 201,
                'body': json.dumps({
                    'all_budget_alerts': all_budgets_alerts
                }, cls = DecimalEncoder)
            }
    except ValidInputError as e:
        print(f'ValidInputError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}