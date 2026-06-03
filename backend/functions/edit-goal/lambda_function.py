from datetime import datetime, date
import json

from input_sanitize import *
from errors import *

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
    #    }
    #  } 
    try:
        fields = event.get('body')
        goal_id = sanitize_id(fields.get('goal_id'))

        # This sends a full request, not just the changes
        start_date = sanitize_date(fields.get('start_date'))
        end_date = sanitize_date(fields.get('end_date'))
        if (start_date > end_date):
            raise ValidInputError('Start date cannot be ahead of the end date')
        description = sanitize_description(fields.get('description')) if fields.get('description') else None
        goal = {
            'user_id': sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
            'goal_id': goal_id,
            'amount' : sanitize_amount(fields.get('amount')),
            'name' : sanitize_type(fields.get('name')),
            'description' : description,
            'start_date' : start_date,
            'end_date' : end_date,
        }
        # Save to database
        
        edit_goal(goal)
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Goal edited successfully',
                'goal_id': goal_id
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
