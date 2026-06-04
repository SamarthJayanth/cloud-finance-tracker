import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
from expense_queries import *

def lambda_handler(event, context):
    # Retrieve expenses given certain criteria
    # By type, date range, amount range, or all expenses 
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'min_amount' : 'num' 
    #       'max_amount': 'num'
    #       'expense_type': 'str'
    #       'start_date': 'YYYY-MM-DD' default is 2000-01-01
    #       'end_date': 'YYYY-MM-DD' default is current day
    #    }
    #  } 
    try:
        fields = event.get('body')
        query_type = fields.get('search_type')
        expenses = get_expenses(
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
        min_amount = sanitize_amount(fields.get('min_amount')) if fields.get('min_amount') else None,
        max_amount = sanitize_amount(fields.get('max_amount')) if fields.get('max_amount') else None,
        expense_type = sanitize_type(fields.get('expense_type')) if fields.get('expense_type') else None,
        start_date = sanitize_date(fields.get('start_date')) if fields.get('start_date') else None,
        end_date = sanitize_date(fields.get('end_date')) if fields.get('end_date') else None
        )
        return {
            'statusCode': 200,
            'body': json.dumps({
            'expenses': expenses, # Need to convert from decimal to float
            'count': len(expenses)
        }, cls = DecimalEncoder)
    }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}