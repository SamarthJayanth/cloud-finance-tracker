from datetime import datetime, date
import json

from input_sanitize import *
from errors import *

def lambda_handler(event, context):
    # Edits the details of a previously made income
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'name': 'str'
    #       'start_date': 'YYYY-MM-DD'
    #       'period': 'str' one of allotted types
    #       'description': 'str'
    #       'id': 'str'
    #    }
    #  } 
    try:
        fields = event.get('body')
        income_id = fields.get('id')

        income = {
            'id' : income_id,
            'amount' : sanitize_amount(fields.get('amount')),
            'period' : sanitize_period(fields.get('period'), 'income'),
            'name' : sanitize_name(fields.get('name')),
            'start_date' : sanitize_date(fields.get('date')),
            'description': sanitize_type(fields.get('description'))
        }

        edit_income(income)
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Income edited successfully',
                'income_id': income_id
            })
        }
        
        #Save back to database
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except NotFoundError as e:
        return {'statusCode': 404, 'body': json.dumps({'error': str(e)})}
    except Exception:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}
