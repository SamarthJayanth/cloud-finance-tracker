import json
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from input_sanitize import *
from budget_queries import *
from expense_queries import *
from budget_utils import *
def lambda_handler(event, context):
    # Receives a budget and determines certain statistics
    # Ensures it is a valid budget, then determines the following:
    # How much is spent/remaining, how many days elpased/remain, etc
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'id' : 'str'
    #    }
    #  } 
    try:
        fields = event.get('body')
        budget_id = sanitize_id(fields.get('budget_id'))
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
        budget = get_budget_by_id(user_id, budget_id)
        start_date, end_date = get_current_period(budget)
        start_date = str(start_date)
        end_date = str(end_date)
        spent = get_total_expenses(
            user_id = user_id,
            start_date = start_date,
            end_date = end_date,
            expense_type = budget.get('type')
        )
        limit = budget.get('amount')

        status = calculate_budget_status(spent, limit, start_date, end_date)
        return {
                'body': json.dumps({
                    'user_id': event['requestContext']['authorizer']['claims']['sub'],
                    'budget_id':   budget_id,
                    'budget_name': budget.get('name'),
                    'period':      budget.get('period'),
                    'start_date':  start_date,
                    'end_date':    end_date,
                    **status
                }, cls = DecimalEncoder)
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}