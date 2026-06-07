from datetime import datetime, date
import json

from input_sanitize import *
from errors import *
from goal_queries import *

def lambda_handler(event, context):
    # Edits the details of a previously made goal
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
    #       'end_date': 'YYYY-MM-DD'
    #       'description': 'str'
    #       'goal_id': 'str'
    #       'type': 'str'
    #    }
    #  } 
    try:
        fields = json.loads(event.get('body') or '{}')
        goal_id = sanitize_id(fields.get('goal_id'))

        # This sends a full request, not just the changes
        start_date = sanitize_date(fields.get('start_date'))
        end_date = sanitize_date(fields.get('end_date'), allow_future = True)
        if (start_date > end_date):
            raise ValidInputError('Start date cannot be ahead of the end date')
        description = sanitize_description(fields.get('description')) if fields.get('description') else None
        goal = {
            'user_id': sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
            'goal_id': goal_id,
            'amount' : sanitize_amount(fields.get('amount')),
            'name' : sanitize_name(fields.get('name')),
            'description' : description,
            'start_date' : start_date,
            'end_date' : end_date,
            'type': sanitize_type(fields.get('type'), is_goal = True)
        }
        # Save to database
        
        edit_goal(goal)
        return {
            'statusCode': 201,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'Goal edited successfully',
                'goal': goal
            }, cls = DecimalEncoder)
        }
        
        #Save back to database
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