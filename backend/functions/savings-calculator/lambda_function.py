import json
import uuid
from datetime import date
from decimal import Decimal # DynamoDB doesn't take float values
from input_sanitize import * # comes from layer automatically
from errors import * # comes from layer automatically
from income_queries import *
from expense_queries import *



def lambda_handler(event, context):
    # Returns how much has been saved in a certain period of time
    # Date is optional
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'start_date': 'str'
    #       'end_date': 'str'
    #    }
    #  } 
    try:
        fields = event.get('body') if event.get('body') else {}
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        kwargs = {}
        # Want to check if start date is non empty but also assign it
        # Also need to know which arguments to pass through, use kwargs
        if(start_date := fields.get('start_date')):
            kwargs['start_date'] = sanitize_date(start_date)
        if (end_date := fields.get('end_date')):
            kwargs['end_date'] = sanitize_date(end_date)
        if (start_date and end_date) and (start_date > end_date):
            raise ValidInputError('Start date cannot be ahead of the end date')
        total_income = get_total_income(user_id = user_id, **kwargs)
        total_expense = get_total_expenses(user_id = user_id, **kwargs)
        return {
            'body': json.dumps({
                'total_savings': total_income-total_expense,
                'period': {'start_date': start_date, 'end_date': end_date}
            }, cls = DecimalEncoder)
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}

    