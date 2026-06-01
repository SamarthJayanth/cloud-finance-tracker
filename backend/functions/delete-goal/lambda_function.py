import json

def lambda_handler(event: dict):
    # Deletes a goal from database
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'id': 'str'
    #    }
    #  } 
    try:
        fields = event.get('body')
        goal_id = fields.get('id')
        if not goal_id:
            return ValueError('Id is invalid')
        # Need id to get the actual goal id
        # For proper security, we must ensure that the request is sent by an authorized user

        # Remove from data base
        delete_goal(goal_id)
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Goal deleted successfully',
                'goal_id': goal_id
            })
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}