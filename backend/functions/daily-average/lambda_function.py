import sys
import os
import json
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))
from input_sanitize import *
from expense_queries import *

def lambda_handler(event: dict):
    # Calculates the daily average spending in a certain time period
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'type': 'str'
    #       'start_date': 'YYYY-MM-DD' defaults to 2000-01-01
    #       'end_date': 'YYYY-MM-DD' defaults to current day
    #    }
    #  }
    try:
        fields = event.get('body')
        start_date = sanitize_date(fields.get('start_date'))
        end_date = sanitize_date(fields.get('end_date'))
        expenses_type = sanitize_type(fields.get('type')) if fields.get('type') else None 
        delta_days = datetime.strptime(end_date, '%Y-%m-%d').date() - datetime.strptime(start_date, '%Y-%m-%d').date()
        if(delta_days.days < 0):
            raise ValidInputError("Start date must be before end date")
        
        expenses = retrieve_by_type({'start_date': start_date, 'end_date': end_date, 'type':expenses_type})
        amount = 0
        for expense in expenses:
            amount += expense.get('amount')
        return round(amount/(delta_days.days + 1), 2)
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}

    