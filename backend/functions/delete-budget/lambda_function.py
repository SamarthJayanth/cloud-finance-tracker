import json
from input_sanitize import *
from errors import *
from budget_queries import delete_budget

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
        fields = json.loads(event.get('body') or '{}')
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        budget_id = sanitize_id(fields.get('budget_id'))

        # Need id to get the actual budget id
        # For proper security, we must ensure that the request is sent by an authorized user

        # Remove from data base
        delete_budget(user_id, budget_id)
        return {
            'statusCode': 201,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'Budget deleted successfully',
            })
        }
    except ValidInputError as e:
        print(f'ValidInputError: {str(e)}')
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'body': json.dumps({'error': 'A Database error has occurred'})}
    except NotFoundError as e:
        print(f'NotFoundError: {str(e)}')
        return {'body': json.dumps({'error': 'A Resource not found error has occurred'})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}