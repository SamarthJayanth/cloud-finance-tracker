import json
import boto3

from budget_utils import calculate_budget_status, get_current_period
from expense_queries import get_total_expenses
from budget_queries import get_all_budgets
from errors import *

sns = boto3.client('sns', region_name='us-east-2')
topic_arn = 'arn:aws:sns:us-east-2:513408219547:budget-alerts'
def lambda_handler(event, context):
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
        # Retrieve all from database
        all_budgets = get_all_budgets()
        for budget in all_budgets:
            user_id = budget.get('user_id')
            start_date, end_date = get_current_period(budget)
            start_date = str(start_date)
            end_date = str(end_date)
            total_expenses = (get_total_expenses(user_id = user_id, start_date = start_date, end_date = end_date))
            full_status = calculate_budget_status(total_expenses, budget.get('amount', 0), start_date, end_date)
            if (full_status.get('status') == 'warning'):
                sns.publish(
                    TopicArn=topic_arn,
                    Subject=f'Budget Alert: {budget.get('name')}\n',
                    Message=f'Your budget "{budget.get("name")}" is over 80% used.\n'
                            f'Spent: ${total_expenses:.2f} of ${float(budget.get("amount", 0)):.2f}\n' 
                            # Use .2f to round and display 2 decimals always
                            f'Period: {start_date} to {end_date}'
                )
    except ValidInputError as e:
        print(f'ValidInputError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'body': json.dumps({'error': 'A Database error has occurred'})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}