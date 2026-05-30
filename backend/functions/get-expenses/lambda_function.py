import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
from expense_queries import *

def lambda_handler(event: dict):
    # Retrieve expenses given certain criteria
    # By type, date range, amount range, or all expenses 
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'type': 'str'
    #       'date': 'YYYY-MM-DD' default is 2000-01-01
    #       'description': 'str'
    #    }
    #  } 
    try:
        fields = event.get('body')
        query_type = fields.get('type')
        match query_type: 
            case 'all':
                get_all_expenses(fields)
            case'by_date_range':
                get_expenses_by_date_range(fields)
            case 'type':
                get_expenses_by_type(fields)
            case 'type_and_by_amount_range':
                get_expenses_filtered(fields)
            case 'amount_range':
                get_expenses_by_amount_range(fields)
            case _:
                raise ValidInputError('Type of expense search must be one of allotted types')
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}