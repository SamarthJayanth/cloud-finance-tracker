
import json

from input_sanitize import *
from goal_queries import *

def lambda_handler(event, context):
    # Retrieve goals given certain criteria
    # By type, date range, amount range, or all goals 
    # Arguments:
    # event = 
    # {
    #    miscellaneous
    #    user_id: 'str'
    # body = 
    #   {
    #       'name': 'str'
    #       'min_amount' : 'num' 
    #       'max_amount': 'num'
    #       'start_date': 'YYYY-MM-DD' default is 2000-01-01
    #       'end_date': 'YYYY-MM-DD' default is current day
    #    }
    #  } 
    try:
        fields = json.loads(event.get('body', '{}'))
        goals = get_goals(
        user_id = sanitize_id(event['requestContext']['authorizer']['claims']['sub']),
        name = sanitize_name(fields.get('name')) if fields.get('name') else None,
        min_amount = sanitize_amount(fields.get('min_amount')) if fields.get('min_amount') else None,
        max_amount = sanitize_amount(fields.get('max_amount')) if fields.get('max_amount') else None,
        start_date = sanitize_date(fields.get('start_date')) if fields.get('start_date') else None,
        end_date = sanitize_date(fields.get('end_date'), allow_future = True) if fields.get('end_date') else None,
        goal_type = sanitize_type(fields.get('type'), is_goal = True) if fields.get('type') else None
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
            'goals': goals, # Need to convert from decimal to float
            'count': len(goals)
        }, cls = DecimalEncoder)
    }
    except ValidInputError as e:
        return {'body': json.dumps({'error': str(e)})}
    except DataBaseError as e:
        return {'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {'body': json.dumps({'error': 'Internal Server Error'})}