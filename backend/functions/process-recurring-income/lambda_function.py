import json
from datetime import date, datetime
from income_queries import *
from errors import *
import uuid
from calendar import monthrange



def days_in_month(year, month):
    return monthrange(year, month)[1]

def is_payment_due(income: dict, date_today):
    start_date = datetime.strptime(income.get('start_date'), '%Y-%m-%d').date()
    delta_days = (date_today - start_date).days

    match income.get('period'):
        case 'weekly':
            return delta_days % 7 == 0 
        case 'biweekly':
            return delta_days % 14 == 0
        case 'monthly': # Today could be the 28th of Feb, but start date could be 31st of a diff month
            return date_today.day == min(start_date.day, days_in_month(date_today.year, date_today.month))
        case 'quarterly':
            return ((start_date.month - date_today.month) % 3 == 0) and date_today.day == min(start_date.day, days_in_month(date_today.year, date_today.month))
        case 'yearly':
            return (start_date.month == date_today.month) and date_today.day == min(start_date.day, days_in_month(date_today.year, date_today.month))
        case _:
            return False
def lambda_handler(event, context):
    # Triggered to add incomes daily
    # Meant to be triggered by EventBridge
    # Adds an income to database if the payment due date is today
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #    }
    #  } 
    try:
        recurring_incomes = get_recurring_income()
        date_today = date.today()
        for income in recurring_incomes:
            if(is_payment_due(income, date_today)):
                add_income({
                    'user_id': income.get('user_id'),
                    'income_id': str(uuid.uuid4()),
                    'name': income.get('name'),
                    'start_date': str(date.today()),
                    'amount': income.get('amount'),
                    'description': income.get('description'),
                    'period': 'one-time'
                })
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'body': json.dumps({'error': 'A Database error has occurred'})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}