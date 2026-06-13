import json
import uuid

from input_sanitize import * # comes from layer automatically
from errors import * # comes from layer automatically
from expense_queries import add_expense

# event contains data from the API call
# Will also authenticate users

def lambda_handler(event, context) :
    # Adds an expense to the database
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
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
        fields = json.loads(event.get('body') or '{}')
        description = sanitize_description(fields.get('description')) if fields.get('description') else None
        expense = {
            'user_id': sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
            'name': sanitize_name(fields.get('name')),
            'amount': (sanitize_amount(fields.get('amount'))),
            'type': sanitize_type(fields.get('type')),
            'date': sanitize_date(fields.get('date')),
            'description':description,
            'expense_id': sanitize_id(str(uuid.uuid4()))
        }
        add_expense(expense)
        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps({
                'message': 'Expense added successfully',
                'expense_id': expense.get('expense_id')
            }, cls=DecimalEncoder)
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
        print(f'ValidInputError: {str(e)}')
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        print(f'DataBaseError: {str(e)}')
        return {'statusCode': 502, 'headers': headers, 'body': json.dumps({'error': 'A Database error has occurred'})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': 'Internal Server Error'})}