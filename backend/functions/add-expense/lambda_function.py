import json
import uuid
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *

# event contains data from the API call
# Will also authenticate users

def lambda_handler(event: dict) :
    # Adds an expense to the database
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'type': 'str'
    #       'date': 'YYYY-MM-DD' default is 2000-01-01
    #       'description': 'str'
    #       'name': 'str'
    #    }
    #  } 

    # fields = json.loads(event.get('body')) for an API call
    try: 
        fields = event.get('body')
        amount =  sanitize_amount(fields.get('amount'))
        expense_type = sanitize_type(fields.get('type'))
        date = sanitize_date(fields.get('date'))
        description = sanitize_description(fields.get('description'))
        expense_id = str(uuid.uuid4())
        name = sanitize_name(fields.get('name'))
        expense = {
            'name': name,
            'amount':amount,
            'type':expense_type,
            'date':date,
            'description':description,
            'id': expense_id
        }
        #Save to Database
        return {
            #'statusCode'
            'body': json.dumps({
                'message': 'Expense added successfully',
                'expense': expense
            })
        }
    except ValidInputError as e:
        return {'body': str(e)}
    except DataBaseError as e:
        return {'body': str(e)}
    except Exception:
        return {'body': json.dumps({'error': 'Internal Server Error'})}
    # Save to DataBase
