import json
import uuid
from decimal import Decimal # DynamoDB doesn't take float values
from input_sanitize import * # comes from layer automatically
from errors import * # comes from layer automatically


# event contains data from the API call
# Will also authenticate users

def lambda_handler(event, context) :
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
    #       'description': 'str' optional
    #       'name': 'str'
    #    }
    #  } 

    # fields = json.loads(event.get('body')) for an API call
    try: 
        fields = event.get('body')
        description = sanitize_description(fields.get('description')) if fields.get('description') else None
        expense = {
            'name': sanitize_name(fields.get('name')),
            'amount': Decimal(round(sanitize_amount(fields.get('amount')), 2)),
            'type': sanitize_type(fields.get('type')),
            'date': sanitize_date(fields.get('date')),
            'description':description,
            'id': str(uuid.uuid4())
        }
        add_expense(expense)
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Expense added successfully',
                'expense': expense
            })
        }
        #Save to Database
        # try:
        #     table.put_item(Item = expense)
        # except Exception as e:
        #     print(f'DynamoDB error: {str(e)}')
        #     raise DataBaseError('Failed to save expense')
        # return {
        #     'statusCode': 201,
        #     'body': json.dumps({
        #         'message': 'Expense added successfully',
        #         'expense': expense
        #     })
        # }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}
