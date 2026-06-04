import json
import uuid
from datetime import date, datetime

from input_sanitize import *
from errors import *
from goal_queries import *
def lambda_handler(event, context):
    # Sets a goal for a user to hit 
    # Goal is an amount saved in some time
     # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'name': 'str'
    #       'start_date': 'str'
    #       'end_date': 'str'
    #       'description': 'str' optional
    #    }
    #  } 
    try:
        fields = event.get('body')
        description = sanitize_description(fields.get('description')) if fields.get('description') else None
        start_date = sanitize_date(fields.get('start_date'))
        end_date = sanitize_date(fields.get('end_date'), allow_future = True)
        if (start_date > end_date):
            raise ValidInputError('Start date cannot be ahead of the end_date')
        goal = {
            'user_id': sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
            'amount' : sanitize_amount(fields.get('amount')),
            'name' : sanitize_name(fields.get('name')),
            'start_date': start_date,
            'end_date': end_date,
            'description': description,
            'goal_id': sanitize_id(str(uuid.uuid4()))
        }
        add_goal(goal)
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Goal added successfully',
                'goal_id': goal.get('goal_id')
            }, cls = DecimalEncoder)
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}
        # Save to database