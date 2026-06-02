import json
import uuid
from datetime import date, datetime

from input_sanitize import *
from errors import *

def lambda_handler(event: dict):
    # Sets a goal for a user to hit 
    # Goal is an amount saved in some time
     # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'name': 'str'
    #       'start_date': 'str'
    #       'end_date': 'str'
    #       'description': 'str'
    #    }
    #  } 
    try:
        fields = event.get('body')
        description = sanitize_description(fields.get('description')) if fields.get('description') else None
        start_date = sanitize_date(fields.get('start_date'))
        end_date = sanitize_date(fields.get('end_date')),
        if (start_date > end_date):
            raise ValidInputError('Start date cannot be ahead of the end_date')
        goal = {
            'amount' : sanitize_amount(fields.get('amount')),
            'name' : sanitize_name(fields.get('name')),
            'start_date': start_date,
            'end_date': end_date,
            'description': description,
            'id': str(uuid.uuid4())
        }
        add_goal(goal)
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Goal added successfully',
                'goal': goal
            })
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        print(f'Unexpected rrror: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}
        # Save to database