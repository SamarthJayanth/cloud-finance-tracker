import json

def lambda_handler(event, context):
    # Deletes a budget from database
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
        budget_id = fields.get('id')
        if not budget_id:
            return ValueError('Id is invalid')
        # Need id to get the actual budget id
        # For proper security, we must ensure that the request is sent by an authorized user

        # Remove from data base
        delete_budget(budget_id)
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