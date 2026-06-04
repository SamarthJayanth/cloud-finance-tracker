import json

def lambda_handler(event, context):
    # Deletes an expense from database
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'expense_id': 'str'
    #    }
    #  } 
    try:
        fields = event.get('body')
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub'])
        expense_id = sanitize_id(fields.get('expense_id'))
        # Need id to get the actual expense id
        # For proper security, we must ensure that the request is sent by an authorized user

        # Remove from data base
        delete_expense(user_id, expense_id)
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Expense deleted successfully',
            })
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}