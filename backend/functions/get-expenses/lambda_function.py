import sys
import os

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
                retrieve_all(fields)
            case'by_date_range':
                retrieve_by_date_range(fields)
            case 'type':
                retrieve_by_type(fields)
            case 'type_and_by_amount_range':
                retrieve_by_type_and_amount_range(fields)
            case 'amount_range':
                retrieve_by_amount_range(fields)
            case _:
                raise ValidInputError('Type of search must be one of allotted types')
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}