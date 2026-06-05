import json
from input_sanitize import *
from errors import *
from budget_queries import *

def lambda_handler(event, context):
    # Deletes a budget from database
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'budget_id': 'str'
    #    }
    #  } 
    try:
        fields = json.loads(event.get('body', '{}'))
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        budget_id = sanitize_id(fields.get('budget_id'))

        # Need id to get the actual budget id
        # For proper security, we must ensure that the request is sent by an authorized user

        # Remove from data base
        delete_budget(user_id, budget_id)
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Budget deleted successfully',
            })
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}