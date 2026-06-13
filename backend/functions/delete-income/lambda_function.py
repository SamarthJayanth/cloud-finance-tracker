import json
from input_sanitize import *
from errors import *
from income_queries import delete_income

def lambda_handler(event, context):
    # Deletes an income from database
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'income_id': 'str'
    #    }
    #  } 
    try:
        fields = json.loads(event.get('body') or '{}')
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        income_id = sanitize_id(fields.get('income_id'))
        # Need id to get the actual income id
        # For proper security, we must ensure that the request is sent by an authorized user

        # Remove from data base
        delete_income(user_id, income_id)
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Income deleted successfully',
            })
        }
    except ValidInputError as e:
        print(f'ValidInputError: {str(e)}')
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'statusCode': 502, 'headers': headers, 'body': json.dumps({'error': 'A Database error has occurred'})}
    except NotFoundError as e:
        print(f'NotFoundError: {str(e)}')
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'A Resource not found error has occurred'})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': 'Internal Server Error'})}