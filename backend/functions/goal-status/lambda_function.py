import json
import math
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

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
    #   user_id: 'str'
    #   body =
    #   {
    #       'goal_id': 'str'
    #   }
    # }
    try:
        fields = json.loads(event.get('body') or '{}')
        goal_id = sanitize_id(fields.get('goal_id'))
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        goal = get_goal_by_id(user_id, goal_id)
        goal_amount = goal.get('amount')
        start_date = goal.get('start_date')
        end_date = goal.get('end_date')
        total_income = get_total_income(user_id = user_id, start_date = sanitize_date(start_date), end_date = str(date.today()))
        total_expense = get_total_expenses(user_id = user_id, start_date = sanitize_date(start_date), end_date = str(date.today()))
        status = calculate_goal_status(amount_spent = total_expense, income_earned = total_income, target_savings = goal_amount, start_date = start_date, end_date = end_date)
        return {
            'statusCode': 201,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                    'user_id': user_id,
                    'goal_id':   goal_id,
                    'name': goal.get('name'),
                    'start_date':  start_date,
                    'end_date':    end_date,
                    'description': goal.get('description'),
                    'type': goal.get('type'),
                    **status
                }, cls = DecimalEncoder)
        }
    except ValidInputError as e:
        print(f'ValidInputError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except NotFoundError as e:
        print(f'NotFoundError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}