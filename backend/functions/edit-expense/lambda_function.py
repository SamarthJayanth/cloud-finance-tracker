import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *

def lambda_handler(event: dict):
    # Edits a previously added expense
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'name': 'str'
    #       'amount' : 'num' 
    #       'type': 'str'
    #       'date': 'YYYY-MM-DD'
    #       'description': 'str'
    #       'id': 'str'
    #    }
    #  } 
    # fields = json.loads(event.get('body')) for an API call
    try:    
        fields = event.get('body')
        name = sanitize_name(fields.get('name'))
        amount =  sanitize_amount(fields.get('amount'))
        expense_type = sanitize_type(fields.get('type'))
        date = sanitize_date(fields.get('date'))
        description = sanitize_description(fields.get('description'))
        expense_id = fields.get('id')
        #Event body has expense id

        # Retrieve expense from database

        expense = { # This is placeholder for retreived one
            'amount':1,
            'type':'food',
            'date':'2024-01-02',
            'description':'To eat',
            'id':'a3f8c2d2-9b4e-4f7a-8c3d-1e2f5a6b7c8d'
            'name' 'Mcdonald'
        }
        expense['amount'] = amount
        expense['type'] = expense_type
        expense['date'] = date
        expense['description'] = description
        expense['name'] = name
        
        
        #Save back to database
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}
