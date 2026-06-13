import json

from input_sanitize import *
from budget_queries import get_budget_by_id
from expense_queries import get_total_expenses
from budget_utils import get_current_period, calculate_budget_status
from errors import *
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
        fields = json.loads(event.get('body') or '{}')
        budget_id = sanitize_id(fields.get('budget_id'))
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        budget = get_budget_by_id(user_id = user_id, budget_id = budget_id)
        start_date, end_date = get_current_period(budget)
        start_date = str(start_date)
        end_date = str(end_date)
        spent = get_total_expenses(
            user_id = user_id,
            start_date = start_date,
            end_date = end_date,
            expense_type = budget.get('type') if budget.get('type') != 'any' else None
        )
        limit = float(budget.get('amount'))

        status = calculate_budget_status(spent, limit, start_date, end_date)
        return {
            'statusCode': 200,
            'headers': headers,
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
    except ExpiredError as e:
        return {'statusCode': 200, 'headers': headers, 'body': json.dumps({{'expired': True, 'message': 'This budget has expired'}})}
    except ValidInputError as e:
        print(f'ValidInputError: {str(e)}')
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'statusCode': 502, 'headers': headers, 'body': json.dumps({'error': 'A Database error has occurred'})}
    except NotFoundError as e:
        print(f'NotFoundError: {str(e)}')
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'A Resource not found error has occurred'})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': 'Internal Server Error'})}