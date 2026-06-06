import json
from input_sanitize import *
from errors import *
from goal_queries import *

def lambda_handler(event, context):
    # Deletes a goal from database
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #     user_id: 'str'
    # body = 
    #   {
    #       'goal_id': 'str'
    #    }
    #  } 
    try:
        fields = json.loads(event.get('body', '{}'))
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        goal_id = sanitize_id(fields.get('goal_id'))

        # Need id to get the actual goal id
        # For proper security, we must ensure that the request is sent by an authorized user

        # Remove from data base
        delete_goal(user_id, goal_id)
        return {
            'statusCode': 201,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'Goal deleted successfully',
            })
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}