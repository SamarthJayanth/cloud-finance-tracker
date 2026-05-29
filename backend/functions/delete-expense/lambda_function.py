import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

def lambda_handler(event: dict):
    # Deletes an expense from database
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
        expense_id = fields.get('id')
        if not expense_id:
            return ValueError('Id is invalid')
        # Need id to get the actual expense id
        # For proper security, we must ensure that the request is sent by an authorized user

        # Remove from data base
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}