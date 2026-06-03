import json

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
        fields = event.get('body')
        user_id = event['requestContext']['authorizer']['claims']['sub']
        budget_id = fields.get('budget_id')
        if not budget_id:
            return ValueError('Budget_id is invalid')
        # Need id to get the actual budget id
        # For proper security, we must ensure that the request is sent by an authorized user

        # Remove from data base
        delete_budget(user_id, budget_id)
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Budget deleted successfully',
                'budget_id': budget_id
            })
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}