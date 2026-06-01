import json
import uuid

from input_sanitize import *
def lambda_handler(event: dict):
    # Receives input details of a specific budget from user
    # Assigns an id and stores to database
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    # body = 
    #   {
    #       'amount' : 'num' 
    #       'type': 'str'
    #       'date': 'YYYY-MM-DD' 
    #       'name': 'str'
    #       'period': 'str' one of allotted types
    #       'is_recurring': 'bool'
    #    }
    #  } 
    try:
        fields = event.get('body')
        # Set a budget, can choose what category to use for this budget
        # Type can be for a timeframe, certain expense types, etc
        description = sanitize_description(fields.get('description')) if fields.get('description') else None
        budget = {
            'amount' : sanitize_amount(fields.get('amount')),
            'start_date' : sanitize_date(fields.get('date')),
            'period' : sanitize_period(fields.get('period')),
            'type' : sanitize_type(fields.get('type')),
            'name' : sanitize_name(fields.get('name')),
            'id' : str(uuid.uuid4()),
            'is_recurring' : sanitize_recurring(fields.get('is_recurring')),
            'description': description
        }
        add_budget(budget)
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Budget added successfully',
                'budget': budget
            })
        }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}